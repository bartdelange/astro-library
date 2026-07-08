## Releases

Releases are automated with the repository-owned script at `scripts/release.py`.
It bumps the backend version, frontend `package.json`, and frontend
`package-lock.json` to the same version, then creates a release commit and
annotated tag. By default it also pushes the branch and tag and creates a
GitHub release with generated notes.

Run it from the repository root with a clean working tree:

```sh
python scripts/release.py patch
```

Or run it without arguments for an interactive flow, which is convenient as a
WebStorm run configuration:

```sh
python scripts/release.py
```

The first argument can be `major`, `minor`, `patch`, or an explicit version:

```sh
python scripts/release.py 1.2.3
```

Useful options:

```sh
python scripts/release.py patch --dry-run
python scripts/release.py patch --no-publish
python scripts/release.py patch --skip-checks
```

Before using it, make sure the GitHub CLI is authenticated:

```sh
gh auth login
gh auth status
```

Creating the GitHub release triggers the Docker image workflow, which publishes
the app image to GitHub Container Registry.
