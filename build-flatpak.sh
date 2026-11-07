#!/bin/bash
# Build, lint and test script for development and pre-submission checks.
#
# Note: the Flatpak manifest pulls sources from the v1.1.0 git tag, so a
# full `flatpak-builder` run requires the tag to exist on GitHub.
# The lint/validate/pytest steps below always run locally.

set -e

echo "Linting Python code..."
python3 -m flake8 eisenhower_matrix/ tests/ --max-line-length=120 --extend-ignore=E203,W503 || true
python3 -m black --check eisenhower_matrix/ tests/ || true

echo "Running tests..."
python3 -m pytest tests/ -q

echo "Validating desktop file..."
desktop-file-validate io.github.alesima.eisenhower.desktop

echo "Validating AppStream metadata..."
appstreamcli validate --no-net io.github.alesima.eisenhower.metainfo.xml

if [ -f "io.github.alesima.eisenhower.yml" ]; then
    echo "Building Flatpak (requires pushed v1.1.0 tag)..."
    flatpak-builder --user --install --force-clean build-dir io.github.alesima.eisenhower.yml
    echo "Run with: flatpak run io.github.alesima.eisenhower"
else
    echo "Flatpak manifest not found"
    exit 1
fi
