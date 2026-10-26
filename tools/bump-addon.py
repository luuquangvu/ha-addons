"""Bump an add-on's version, Dockerfile pin, and changelog after an upstream update."""

import json
import os
import pathlib
import re
import subprocess
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from functools import partial
from typing import Any

import yaml

CALLOUT_NOTE = (
    "> [!NOTE]\n"
    "> If you find this addon useful, please consider giving it a ⭐ on"
    " [GitHub](https://github.com/luuquangvu/ha-addons) to support my work"
    " and help others discover it. Thank you very much! ❤️"
)


def get_env(name: str) -> str:
    """Return the named environment variable, exiting with a GitHub Actions error if unset."""
    val = os.environ.get(name)
    if not val:
        print(f"::error::Environment variable {name} not set")
        sys.exit(1)
    return val


def extract_available_platforms(raw_manifest: dict[str, Any]) -> set[str]:
    """Extract supported OS and architecture platform strings from an image manifest."""
    available_platforms: set[str] = set()
    if "manifests" in raw_manifest:
        for m in raw_manifest["manifests"]:
            p = m["platform"]
            available_platforms.add(f"{p['os']}/{p['architecture']}")
            if "variant" in p:
                available_platforms.add(f"{p['os']}/{p['architecture']}/{p['variant']}")
        return available_platforms

    os_name = raw_manifest.get("os") or raw_manifest.get("Os")
    arch = raw_manifest.get("architecture") or raw_manifest.get("Architecture")

    if not os_name or not arch:
        print("::error::Unexpected manifest structure: missing OS or Architecture information.")
        sys.exit(1)

    available_platforms.add(f"{os_name}/{arch}")
    return available_platforms


def validate_architectures(data: dict[str, Any], manifest_file_path: str) -> None:
    """Validate that required architectures are supported by the upstream manifest."""
    ha_arch_map = {"amd64": "linux/amd64", "aarch64": "linux/arm64"}

    required_archs = data.get("arch", [])
    if unknown_archs := [a for a in required_archs if a not in ha_arch_map]:
        print(f"::error::Unsupported arch value(s) in config: {', '.join(unknown_archs)}")
        sys.exit(1)

    required_platforms = [ha_arch_map[a] for a in required_archs]

    manifest_file = pathlib.Path(manifest_file_path)
    if not manifest_file.exists():
        print(f"::error::Manifest file not found: {manifest_file_path}")
        sys.exit(1)

    with open(manifest_file, encoding="utf-8") as f:
        raw_manifest = json.load(f)

    available_platforms = extract_available_platforms(raw_manifest)

    print(f"Required: {required_platforms}")
    print(f"Available: {available_platforms}")

    if missing := [
        req
        for req in required_platforms
        if not any(avail == req or avail.startswith(f"{req}/") for avail in available_platforms)
    ]:
        print(f"::error::Upstream lacks required platforms: {missing}")
        sys.exit(1)

    print("Architecture check passed.")


def bump_version(config_path: pathlib.Path, data: dict[str, Any]) -> str:
    """Increment the patch version in config.yaml and return the new version string."""
    ver = str(data.get("version", "0.0.0"))
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", ver)
    if not m:
        print(f"::error::Unsupported version format: {ver}")
        sys.exit(1)

    major, minor, patch = map(int, m.groups())
    new_ver = f"{major}.{minor}.{patch + 1}"
    data["version"] = new_ver

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

    print(f"Bumped version from {ver} to {new_ver}")
    return new_ver


def check_tag(image_name: str, tag: str) -> tuple[str, str | None]:
    """Inspect a remote image tag and return its digest if found."""
    try:
        cmd = [
            "skopeo",
            "inspect",
            "--format",
            "{{.Digest}}",
            f"docker://{image_name}:{tag}",
        ]
        res = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=10)
        if res.returncode == 0:
            digest = res.stdout.strip()
            return tag, digest or None
    except subprocess.TimeoutExpired:
        print(f"Timeout checking tag: {tag}")
    except (subprocess.SubprocessError, OSError) as e:
        print(f"Error checking tag {tag}: {e}")
    return tag, None


def find_matching_tag(image_name: str, target_digest: str) -> str | None:
    """Search for a specific date-formatted version tag matching the target digest."""
    print("Attempting to find a specific tag matching the latest digest...")
    try:
        res = subprocess.run(
            ["skopeo", "list-tags", f"docker://{image_name}"],
            capture_output=True,
            text=True,
            check=True,
        )
        tags_data = json.loads(res.stdout)
        all_tags = tags_data.get("Tags", [])

        pattern = re.compile(r"^\d{8}-[a-f0-9]+$")
        version_tags = [t for t in all_tags if pattern.match(t)]
        version_tags.sort(reverse=True)
        tags_to_check = version_tags[:10]

        print(f"Checking {len(tags_to_check)} tags in parallel...")
        check_func = partial(check_tag, image_name)
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(check_func, tags_to_check))

        for tag, t_digest in results:
            if t_digest == target_digest:
                print(f"Found matching version tag: {tag}")
                return tag
    except (
        subprocess.SubprocessError,
        OSError,
        json.JSONDecodeError,
        KeyError,
        re.error,
    ) as e:
        print(f"Error finding matching tag: {e}")

    return None


def update_dockerfile(
    dockerfile_path: pathlib.Path,
    image_name: str,
    new_ver: str,
    new_tag: str | None,
) -> None:
    """Update Dockerfile base image tag and io.hass.version label."""
    try:
        content = dockerfile_path.read_text(encoding="utf-8")
        if new_tag:
            image_pattern = re.escape(image_name)
            new_content = re.sub(
                rf"^FROM\s+{image_pattern}(?::[^\s]+|@[^\s]+)?(.*)$",
                f"FROM {image_name}:{new_tag}\\1",
                content,
                flags=re.MULTILINE,
            )
            new_content = re.sub(
                r'(io\.hass\.version=["\'])([^"\']+)(["\'])',
                rf"\g<1>{new_ver}\g<3>",
                new_content,
            )
            dockerfile_path.write_text(new_content, encoding="utf-8")
            print(f"Updated {dockerfile_path} to use tag {new_tag} and version {new_ver}")
        else:
            print("No matching specific tag found. Updating Dockerfile version label only.")
            new_content = re.sub(
                r'(io\.hass\.version=["\'])([^"\']+)(["\'])',
                rf"\1{new_ver}\3",
                content,
            )
            if new_content != content:
                dockerfile_path.write_text(new_content, encoding="utf-8")
                print(f"Updated {dockerfile_path} with new version {new_ver}")
            else:
                print("Dockerfile already up to date.")
    except (OSError, re.error) as e:
        print(f"Error updating Dockerfile: {e}")


def update_changelog(addon_dir: pathlib.Path, new_ver: str, upstream_ver: str) -> None:
    """Update CHANGELOG.md with a new version entry while preserving the header callout."""
    changelog_path = addon_dir / "CHANGELOG.md"
    old_content = ""
    if changelog_path.exists():
        old_content = changelog_path.read_text(encoding="utf-8")

    today = datetime.now(UTC).date().isoformat()
    new_entry = (
        f"## {new_ver} - {today}\n\n"
        f"- Update version to {upstream_ver}\n"
        f"- Cập nhật phiên bản lên {upstream_ver}\n\n"
    )

    if content := old_content.strip():
        if "> [!NOTE]" not in content:
            content = (
                content.replace("# Changelog", f"# Changelog\n\n{CALLOUT_NOTE}", 1)
                if "# Changelog" in content
                else f"# Changelog\n\n{CALLOUT_NOTE}\n\n{content}"
            )
        if match := re.search(r"^## ", content, re.MULTILINE):
            header = content[: match.start()].rstrip()
            rest = content[match.start() :]
            final_content = f"{header}\n\n{new_entry}{rest}"
        else:
            final_content = f"{content.rstrip()}\n\n{new_entry}"

    else:
        final_content = f"# Changelog\n\n{CALLOUT_NOTE}\n\n{new_entry}"
    changelog_path.write_text(final_content, encoding="utf-8")
    print(f"Updated CHANGELOG.md with version {new_ver}")


def write_github_output(outputs: dict[str, str]) -> None:
    """Write key-value pairs to the GITHUB_OUTPUT environment file if available."""
    github_output = os.environ.get("GITHUB_OUTPUT")
    if not github_output:
        return

    with open(github_output, "a", encoding="utf-8") as f:
        for name, value in outputs.items():
            delimiter = "EOF"
            if "\n" in value or "<<" in value:
                delimiter = f"ghadelimiter_{uuid.uuid4().hex}"
            f.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")


def main() -> None:
    """Bump the add-on's version, pin the Dockerfile to the new image, and update the changelog."""
    addon_dir = pathlib.Path(get_env("ADDON_DIR"))
    config_path = addon_dir / "config.yaml"
    digest_file = pathlib.Path(get_env("DIGEST_FILE"))
    latest_digest = get_env("LATEST_DIGEST")
    image_name = get_env("IMAGE_NAME")
    manifest_file_path = get_env("MANIFEST_FILE")

    if not config_path.exists():
        print(f"::error::Config file not found at {config_path}")
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    validate_architectures(data, manifest_file_path)
    new_ver = bump_version(config_path, data)

    digest_file.parent.mkdir(parents=True, exist_ok=True)
    digest_file.write_text(latest_digest, encoding="utf-8")

    new_tag = find_matching_tag(image_name, latest_digest)
    dockerfile_path = addon_dir / "Dockerfile"
    update_dockerfile(dockerfile_path, image_name, new_ver, new_tag)

    clean_digest = latest_digest.replace("sha256:", "") if latest_digest else ""
    digest_short = f"{clean_digest[:12]}..." if clean_digest else "latest"
    upstream_ver = new_tag or digest_short

    update_changelog(addon_dir, new_ver, upstream_ver)
    write_github_output({"upstream_ver": upstream_ver, "new_ver": new_ver})


if __name__ == "__main__":
    main()
