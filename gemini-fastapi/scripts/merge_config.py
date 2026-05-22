"""Merge config defaults into a user config without overwriting user values."""

from __future__ import annotations

import argparse
import copy
import os
import shutil
import sys
import tempfile
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError


yaml = YAML()
yaml.default_flow_style = False
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.preserve_quotes = True
yaml.representer.add_representer(
    type(None),
    lambda representer, data: representer.represent_scalar(
        "tag:yaml.org,2002:null",
        "null",
    ),
)


def load_yaml(path: Path) -> Any:
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as file:
        data = yaml.load(file)

    return {} if data is None else data


def dump_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        text=True,
    )

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            yaml.dump(data, file)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def is_mapping(value: Any) -> bool:
    return isinstance(value, MutableMapping)


def copy_key_comment(source: Any, target: Any, key: Any) -> None:
    if not hasattr(source, "ca") or not hasattr(target, "ca"):
        return
    if key not in source.ca.items:
        return

    target.ca.items[key] = copy.deepcopy(source.ca.items[key])


def copy_default_value(source: Any) -> Any:
    return copy.deepcopy(source)


def get_list_item_template(value: Any) -> Any:
    if not isinstance(value, list) or not value:
        return None

    first_item = value[0]
    if not is_mapping(first_item):
        return None

    return first_item


def merge_config(
    old_default: Any,
    new_default: Any,
    user_config: Any,
    path: str = "",
    added: list[str] | None = None,
    updated: list[str] | None = None,
    removed: list[str] | None = None,
) -> Any:
    if added is None:
        added = []
    if updated is None:
        updated = []
    if removed is None:
        removed = []

    if is_mapping(new_default) and is_mapping(user_config):
        old_map = old_default if is_mapping(old_default) else {}

        for key, new_value in new_default.items():
            key_path = f"{path}.{key}" if path else str(key)
            if key in user_config:
                old_user_value = copy.deepcopy(user_config[key])
                user_config[key] = merge_config(
                    old_map.get(key),
                    new_value,
                    user_config[key],
                    key_path,
                    added,
                    updated,
                    removed,
                )
                if old_user_value != user_config[key] and old_user_value == old_map.get(
                    key
                ):
                    copy_key_comment(new_default, user_config, key)
            else:
                user_config[key] = copy_default_value(new_value)
                copy_key_comment(new_default, user_config, key)
                added.append(key_path)

        for key, old_value in list(old_map.items()):
            key_path = f"{path}.{key}" if path else str(key)
            if (
                key not in new_default
                and key in user_config
                and user_config[key] == old_value
            ):
                del user_config[key]
                removed.append(key_path)

        return user_config

    if user_config == old_default and user_config != new_default:
        if path:
            updated.append(path)
        return copy_default_value(new_default)

    new_item_template = get_list_item_template(new_default)
    if new_item_template is not None and isinstance(user_config, list):
        old_item_template = get_list_item_template(old_default)

        for index, user_item in enumerate(user_config):
            if not is_mapping(user_item):
                continue

            item_path = f"{path}[{index}]"
            user_config[index] = merge_config(
                old_item_template,
                new_item_template,
                user_item,
                item_path,
                added,
                updated,
                removed,
            )

        return user_config

    return user_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--default", required=True, type=Path)
    parser.add_argument("--user", required=True, type=Path)
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--backup", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not args.default.exists():
        print(f"[WARN] Default config not found: {args.default}", file=sys.stderr)
        return 0

    if not args.user.exists():
        copy_file(args.default, args.user)
        copy_file(args.default, args.state)
        print(f"[INFO] Created user config from {args.default}")
        return 0

    try:
        old_default = load_yaml(args.state)
        new_default = load_yaml(args.default)
        user_config = load_yaml(args.user)
    except YAMLError as error:
        print(f"[ERROR] Failed to parse YAML config: {error}", file=sys.stderr)
        return 1

    added: list[str] = []
    updated: list[str] = []
    removed: list[str] = []
    merge_config(
        old_default,
        new_default,
        user_config,
        added=added,
        updated=updated,
        removed=removed,
    )

    if added or updated or removed:
        copy_file(args.user, args.backup)
        dump_yaml(args.user, user_config)
        print(f"[INFO] Updated user config defaults: {args.user}")
        if added:
            print(f"[INFO] Added config defaults: {', '.join(added)}")
        if updated:
            print(f"[INFO] Updated unchanged config defaults: {', '.join(updated)}")
        if removed:
            print(f"[INFO] Removed unchanged stale defaults: {', '.join(removed)}")
        print(f"[INFO] Previous user config backup: {args.backup}")
    else:
        print("[INFO] User config is already up to date.")

    copy_file(args.default, args.state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
