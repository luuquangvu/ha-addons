import os
import json
import pathlib
import re
import sys
import yaml
import subprocess
import uuid
from datetime import date
from concurrent.futures import ThreadPoolExecutor
from functools import partial


def get_env(name):
    val = os.environ.get(name)
    if not val:
        print(f"::error::Environment variable {name} not set")
        sys.exit(1)
    return val


def main():
    addon_dir = pathlib.Path(get_env("ADDON_DIR"))
    config_path = addon_dir / "config.yaml"
    digest_file = pathlib.Path(get_env("DIGEST_FILE"))
    latest_digest = get_env("LATEST_DIGEST")
    image_name = get_env("IMAGE_NAME")

    if not config_path.exists():
        print(f"::error::Config file not found at {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    ha_arch_map = {"amd64": "linux/amd64", "aarch64": "linux/arm64"}

    required_archs = data.get("arch", [])
    unknown_archs = [a for a in required_archs if a not in ha_arch_map]
    if unknown_archs:
        print(
            f"::error::Unsupported arch value(s) in config: {', '.join(unknown_archs)}"
        )
        sys.exit(1)

    required_platforms = [ha_arch_map[a] for a in required_archs]

    manifest_file_path = os.environ.get("MANIFEST_FILE")
    if not manifest_file_path:
        print("::error::Environment variable MANIFEST_FILE not set")
        sys.exit(1)

    manifest_file = pathlib.Path(manifest_file_path)
    if not manifest_file.exists():
        print(f"::error::Manifest file not found: {manifest_file_path}")
        sys.exit(1)

    with open(manifest_file, "r") as f:
        raw_manifest = json.load(f)

    available_platforms = set()
    if "manifests" in raw_manifest:
        for m in raw_manifest["manifests"]:
            p = m["platform"]
            available_platforms.add(f"{p['os']}/{p['architecture']}")
            if "variant" in p:
                available_platforms.add(f"{p['os']}/{p['architecture']}/{p['variant']}")
    else:
        os_name = raw_manifest.get("os") or raw_manifest.get("Os")
        arch = raw_manifest.get("architecture") or raw_manifest.get("Architecture")

        if not os_name or not arch:
            print(
                "::error::Unexpected manifest structure: missing OS or Architecture information."
            )
            sys.exit(1)

        available_platforms.add(f"{os_name}/{arch}")

    print(f"Required: {required_platforms}")
    print(f"Available: {available_platforms}")

    missing = []
    for req in required_platforms:
        if not any(
            avail == req or avail.startswith(f"{req}/") for avail in available_platforms
        ):
            missing.append(req)

    if missing:
        print(f"::error::Upstream lacks required platforms: {missing}")
        sys.exit(1)

    print("Architecture check passed.")

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

    digest_file.parent.mkdir(parents=True, exist_ok=True)
    digest_file.write_text(latest_digest, encoding="utf-8")

    print("Attempting to find a specific tag matching the latest digest...")
    target_digest = latest_digest
    dockerfile_path = addon_dir / "Dockerfile"
    new_tag = None

    def check_tag(tag, image_name):
        try:
            cmd = [
                "skopeo",
                "inspect",
                "--format",
                "{{.Digest}}",
                f"docker://{image_name}:{tag}",
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if res.returncode == 0:
                digest = res.stdout.strip()
                return tag, digest or None
        except subprocess.TimeoutExpired:
            print(f"Timeout checking tag: {tag}")
        except Exception as e:
            print(f"Error checking tag {tag}: {e}")
        return tag, None

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
        check_func = partial(check_tag, image_name=image_name)
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(check_func, tags_to_check))

        for tag, t_digest in results:
            if t_digest == target_digest:
                new_tag = tag
                break

        if new_tag:
            print(f"Found matching version tag: {new_tag}")
            content = dockerfile_path.read_text(encoding="utf-8")
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
            print(
                f"Updated {dockerfile_path} to use tag {new_tag} and version {new_ver}"
            )
        else:
            print(
                "No matching specific tag found. Updating Dockerfile version label only."
            )
            content = dockerfile_path.read_text(encoding="utf-8")
            new_content = re.sub(
                r'(io\.hass\.version=["\'])([^"\']+)(["\'])', rf"\1{new_ver}\3", content
            )
            if new_content != content:
                dockerfile_path.write_text(new_content, encoding="utf-8")
                print(f"Updated {dockerfile_path} with new version {new_ver}")
            else:
                print("Dockerfile already up to date.")
    except Exception as e:
        print(f"Error updating Dockerfile: {e}")

    changelog_path = addon_dir / "CHANGELOG.md"
    old_content = ""
    if changelog_path.exists():
        old_content = changelog_path.read_text(encoding="utf-8")

    today = date.today().isoformat()
    clean_digest = target_digest.replace("sha256:", "") if target_digest else ""
    digest_short = f"{clean_digest[:12]}..." if clean_digest else "latest"
    upstream_ver = new_tag or digest_short

    new_entry = f"## {new_ver} - {today}\n\n- Update version to {upstream_ver}\n- Cập nhật phiên bản lên {upstream_ver}\n\n"

    if "# Changelog" in old_content:
        parts = old_content.split("\n", 1)
        header = parts[0]
        rest = parts[1] if len(parts) > 1 else ""
        if rest.startswith("\n"):
            rest = rest[1:]
        final_content = f"{header}\n\n{new_entry}{rest}"
    else:
        final_content = f"# Changelog\n\n{new_entry}{old_content}"

    changelog_path.write_text(final_content, encoding="utf-8")
    print(f"Updated CHANGELOG.md with version {new_ver}")

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            for name, value in [
                ("upstream_ver", upstream_ver),
                ("new_ver", new_ver),
            ]:
                delimiter = "EOF"
                if "\n" in value or "<<" in value:
                    delimiter = f"ghadelimiter_{uuid.uuid4().hex}"
                f.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")


if __name__ == "__main__":
    main()
