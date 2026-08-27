#!/bin/sh
# Install the md-sync pre-commit hook into .git/hooks/.
set -e
REPO=$(git rev-parse --show-toplevel)
mkdir -p "$REPO/.git/hooks"
cp "$REPO/tools/hooks/pre-commit" "$REPO/.git/hooks/pre-commit"
chmod +x "$REPO/.git/hooks/pre-commit"
echo "installed: .git/hooks/pre-commit (md-sync guard)"
