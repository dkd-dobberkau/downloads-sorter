#!/bin/bash
set -e

# Release script for downloads-sorter
# Usage: ./release.sh 0.2.0

if [ -z "$1" ]; then
    echo "Usage: ./release.sh <version>"
    echo "Example: ./release.sh 0.2.0"
    exit 1
fi

VERSION=$1

# Validate version format (basic check)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format X.Y.Z (e.g., 0.2.0)"
    exit 1
fi

echo "Releasing version $VERSION..."

# Update version in pyproject.toml
sed -i '' "s/^version = \".*\"/version = \"$VERSION\"/" pyproject.toml

# Update version in __init__.py
sed -i '' "s/^__version__ = '.*'/__version__ = '$VERSION'/" downloads_sorter/__init__.py

# Show changes
echo ""
echo "Updated files:"
grep -n "version" pyproject.toml | head -1
grep -n "__version__" downloads_sorter/__init__.py

# Git operations
echo ""
echo "Committing and tagging..."
git add pyproject.toml downloads_sorter/__init__.py
git commit -m "Release v$VERSION"
git tag -a "v$VERSION" -m "Release v$VERSION"

echo ""
echo "Done! To publish:"
echo "  git push origin main --tags"
echo "  python -m build"
echo "  twine upload dist/*"
