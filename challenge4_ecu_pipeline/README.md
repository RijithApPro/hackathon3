# Challenge 4 – ECU Release Pipeline

## Overview

An end-to-end release pipeline for ECU (Electronic Control Unit) software,
consisting of:

1. **Python helper** (`ecu_pipeline.py`) – version validation, artifact naming,
   and release-readiness checks.
2. **Makefile** – local `lint → test → build → release` workflow.
3. **GitHub Actions workflow** (`.github/workflows/ecu_release.yml`) –
   CI/CD pipeline with four stages: Lint → Test → Build → Publish Release.

## Repository layout

```
challenge4_ecu_pipeline/
├── VERSION                        # Semantic version: vMAJOR.MINOR.PATCH
├── Makefile                       # Local build automation
├── ecu_pipeline.py                # Pipeline helper module + CLI
├── test_ecu_pipeline.py           # Unit tests
├── README.md                      # This file
└── .github/workflows/
    └── ecu_release.yml            # GitHub Actions workflow
```

## Prerequisites

* Python 3.9 or later
* `make` (for Makefile targets)
* GitHub Actions (for the CI/CD workflow)

## Local usage

### Version management

The current version is stored in `VERSION`:

```
v1.0.0
```

Bump it manually before creating a release tag.

### Makefile targets

| Target | Description |
|--------|-------------|
| `make lint` | Run pylint on `ecu_pipeline.py` |
| `make test` | Run pytest unit tests |
| `make build` | Run release check then build artifact into `dist/` |
| `make release` | Build + package into a `.tar.gz` archive |
| `make clean` | Remove `dist/` and cache files |

```bash
make all          # lint + test + build
make release ECU_ID=BCM   # build and package for a specific ECU
```

### CLI helper

```bash
# Print current version
python ecu_pipeline.py version

# Compute artifact name
python ecu_pipeline.py artifact-name BCM

# Run release readiness check
python ecu_pipeline.py check
```

## CI/CD Pipeline (GitHub Actions)

Triggered on:
* **Pull requests** to `main` – runs Lint, Test, Build stages.
* **Version tags** (`v*.*.*`) – runs all four stages and publishes a GitHub Release.

### Pipeline stages

```
┌─────────┐     ┌───────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Lint   │ ──► │   Test    │ ──► │  Build Artifact │ ──► │ Publish Release │
└─────────┘     └───────────┘     └─────────────────┘     └─────────────────┘
                                                            (tags only)
```

### Creating a release

```bash
# Bump the version
echo "v1.1.0" > VERSION
git add VERSION
git commit -m "chore: bump version to v1.1.0"
git tag v1.1.0
git push origin main --tags
```

GitHub Actions will automatically build and publish the release.

## Tests

```bash
pip install pytest
pytest test_ecu_pipeline.py -v
```
