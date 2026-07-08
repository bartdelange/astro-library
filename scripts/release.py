#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKEND_PYPROJECT = ROOT / "backend" / "pyproject.toml"
FRONTEND_PACKAGE = ROOT / "frontend" / "package.json"
FRONTEND_LOCK = ROOT / "frontend" / "package-lock.json"


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    @classmethod
    def parse(cls, value: str) -> Version:
        match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", value)
        if match is None:
            raise ValueError(f"Expected a semver version like 1.2.3, got {value!r}")

        major, minor, patch = (int(part) for part in match.groups())
        return cls(major=major, minor=minor, patch=patch)

    def bump(self, level: str) -> Version:
        if level == "major":
            return Version(self.major + 1, 0, 0)
        if level == "minor":
            return Version(self.major, self.minor + 1, 0)
        if level == "patch":
            return Version(self.major, self.minor, self.patch + 1)

        return Version.parse(level)

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


def run(command: list[str], *, dry_run: bool = False) -> None:
    print("$", " ".join(command))
    if dry_run:
        return

    subprocess.run(command, cwd=ROOT, check=True)


def capture(command: list[str]) -> str:
    return subprocess.check_output(command, cwd=ROOT, text=True).strip()


def assert_clean_worktree() -> None:
    status = capture(["git", "status", "--porcelain"])
    if status:
        raise RuntimeError(
            "The working tree must be clean before releasing. "
            "Commit or stash your changes first."
        )


def backend_version() -> Version:
    data = tomllib.loads(BACKEND_PYPROJECT.read_text())
    return Version.parse(data["project"]["version"])


def write_backend_version(version: Version, *, dry_run: bool) -> None:
    text = BACKEND_PYPROJECT.read_text()
    updated = re.sub(
        r'(?m)^version = "\d+\.\d+\.\d+"$',
        f'version = "{version}"',
        text,
        count=1,
    )

    if updated == text:
        raise RuntimeError(f"Could not update project.version in {BACKEND_PYPROJECT}")

    print(f"update {BACKEND_PYPROJECT.relative_to(ROOT)} -> {version}")
    if not dry_run:
        BACKEND_PYPROJECT.write_text(updated)


def write_frontend_package_version(version: Version, *, dry_run: bool) -> None:
    for path in (FRONTEND_PACKAGE, FRONTEND_LOCK):
        data = json.loads(path.read_text())
        data["version"] = str(version)

        if path == FRONTEND_LOCK:
            data["packages"][""]["version"] = str(version)

        print(f"update {path.relative_to(ROOT)} -> {version}")
        if not dry_run:
            path.write_text(json.dumps(data, indent=2) + "\n")


def release_exists(tag: str) -> bool:
    result = subprocess.run(
        ["gh", "release", "view", tag],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bump project versions, create a release commit/tag, and publish a GitHub release."
    )
    parser.add_argument(
        "level",
        nargs="?",
        help="Semver bump level: major, minor, patch, or an explicit version like 1.2.3.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes and commands without changing files or creating a release.",
    )
    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Skip the repository pre-commit and pre-push checks before committing.",
    )
    parser.add_argument(
        "--no-publish",
        action="store_true",
        help="Create the release commit and tag locally, but do not push or create the GitHub release.",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Git remote to push to. Defaults to origin.",
    )
    return parser.parse_args()


def ask(question: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    answer = input(f"{question}{suffix}: ").strip()
    if answer:
        return answer
    if default is not None:
        return default

    return ask(question, default)


def ask_yes_no(question: str, *, default: bool) -> bool:
    default_label = "Y/n" if default else "y/N"

    while True:
        answer = input(f"{question} [{default_label}]: ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False

        print("Please answer yes or no.")


def configure_interactively(args: argparse.Namespace) -> argparse.Namespace:
    if args.level is not None:
        return args

    current_version = backend_version()

    print("Interactive release")
    print(f"Current version: {current_version}")
    print()
    print("Choose a semver bump:")
    print(f"  1. patch -> {current_version.bump('patch')}")
    print(f"  2. minor -> {current_version.bump('minor')}")
    print(f"  3. major -> {current_version.bump('major')}")
    print("  4. custom version")

    choice = ask("Selection", "1").lower()
    levels = {
        "1": "patch",
        "patch": "patch",
        "2": "minor",
        "minor": "minor",
        "3": "major",
        "major": "major",
    }

    if choice in {"4", "custom"}:
        args.level = ask("Version")
    elif choice in levels:
        args.level = levels[choice]
    else:
        args.level = choice

    return args


def main() -> int:
    args = configure_interactively(parse_args())
    dry_run = args.dry_run

    if not dry_run:
        assert_clean_worktree()

    current_branch = capture(["git", "branch", "--show-current"])
    current_version = backend_version()
    next_version = current_version.bump(args.level)
    tag = f"v{next_version}"

    print(f"current version: {current_version}")
    print(f"next version:    {next_version}")
    print(f"tag:             {tag}")

    existing_tags = capture(["git", "tag", "--list", tag])
    if existing_tags:
        raise RuntimeError(f"Tag {tag} already exists locally.")

    if not dry_run and not args.no_publish and release_exists(tag):
        raise RuntimeError(f"GitHub release {tag} already exists.")

    write_backend_version(next_version, dry_run=dry_run)
    write_frontend_package_version(next_version, dry_run=dry_run)

    run(["uv", "lock", "--project", "backend"], dry_run=dry_run)

    if not args.skip_checks:
        run(
            ["uv", "--project", "backend", "run", "pre-commit", "run", "--all-files"],
            dry_run=dry_run,
        )
        run(
            [
                "uv",
                "--project",
                "backend",
                "run",
                "pre-commit",
                "run",
                "--all-files",
                "--hook-stage",
                "pre-push",
            ],
            dry_run=dry_run,
        )

    run(
        [
            "git",
            "add",
            "backend/pyproject.toml",
            "backend/uv.lock",
            "frontend/package.json",
            "frontend/package-lock.json",
        ],
        dry_run=dry_run,
    )
    commit_command = ["git", "commit", "-m", f"release: {tag}"]
    push_command = ["git", "push", args.remote, current_branch]
    tag_push_command = ["git", "push", args.remote, tag]

    if not args.skip_checks:
        commit_command.append("--no-verify")
        push_command.insert(2, "--no-verify")
        tag_push_command.insert(2, "--no-verify")

    run(commit_command, dry_run=dry_run)
    run(["git", "tag", "-a", tag, "-m", tag], dry_run=dry_run)

    if not args.no_publish:
        run(push_command, dry_run=dry_run)
        run(tag_push_command, dry_run=dry_run)
        run(
            ["gh", "release", "create", tag, "--title", tag, "--generate-notes"],
            dry_run=dry_run,
        )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
    except Exception as exc:
        print(f"release failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
