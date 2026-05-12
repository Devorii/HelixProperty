#!/bin/bash

# Automatic Git Tagging Script for Semantic Versioning
# Usage: ./git_update.sh -v [major|minor|patch]

set -e

# Default version bump
VERSION_TYPE="patch"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -v|--version)
      VERSION_TYPE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 -v [major|minor|patch]"
      exit 1
      ;;
  esac
done

# Validate version type
if [[ ! "$VERSION_TYPE" =~ ^(major|minor|patch)$ ]]; then
  echo "Error: Version type must be 'major', 'minor', or 'patch'"
  exit 1
fi

# Get the latest tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

# Remove 'v' prefix if present
LATEST_TAG=${LATEST_TAG#v}

# Split version into components
IFS='.' read -ra VERSION_PARTS <<< "$LATEST_TAG"
MAJOR=${VERSION_PARTS[0]}
MINOR=${VERSION_PARTS[1]}
PATCH=${VERSION_PARTS[2]}

# Increment version based on type
case $VERSION_TYPE in
  major)
    MAJOR=$((MAJOR + 1))
    MINOR=0
    PATCH=0
    ;;
  minor)
    MINOR=$((MINOR + 1))
    PATCH=0
    ;;
  patch)
    PATCH=$((PATCH + 1))
    ;;
esac

# Create new tag
NEW_TAG="v${MAJOR}.${MINOR}.${PATCH}"

echo "Latest tag: $LATEST_TAG"
echo "New tag: $NEW_TAG"
echo "Version bump type: $VERSION_TYPE"

# Create and push the new tag
git tag "$NEW_TAG"
git push origin "$NEW_TAG"

# Set output for GitHub Actions
echo "git-tag=$NEW_TAG" >> $GITHUB_OUTPUT