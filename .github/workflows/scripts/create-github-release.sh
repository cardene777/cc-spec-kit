#!/usr/bin/env bash
set -euo pipefail

# create-github-release.sh
# Create a GitHub release with all template zip files
# Usage: create-github-release.sh <version>

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <version>" >&2
  exit 1
fi

VERSION="$1"

# Remove 'v' prefix from version for release title
VERSION_NO_V=${VERSION#v}

gh release create "$VERSION" \
  .genreleases/grove-template-copilot-sh-"$VERSION".zip \
  .genreleases/grove-template-copilot-ps-"$VERSION".zip \
  .genreleases/grove-template-claude-sh-"$VERSION".zip \
  .genreleases/grove-template-claude-ps-"$VERSION".zip \
  .genreleases/grove-template-gemini-sh-"$VERSION".zip \
  .genreleases/grove-template-gemini-ps-"$VERSION".zip \
  .genreleases/grove-template-cursor-agent-sh-"$VERSION".zip \
  .genreleases/grove-template-cursor-agent-ps-"$VERSION".zip \
  .genreleases/grove-template-opencode-sh-"$VERSION".zip \
  .genreleases/grove-template-opencode-ps-"$VERSION".zip \
  .genreleases/grove-template-qwen-sh-"$VERSION".zip \
  .genreleases/grove-template-qwen-ps-"$VERSION".zip \
  .genreleases/grove-template-windsurf-sh-"$VERSION".zip \
  .genreleases/grove-template-windsurf-ps-"$VERSION".zip \
  .genreleases/grove-template-codex-sh-"$VERSION".zip \
  .genreleases/grove-template-codex-ps-"$VERSION".zip \
  .genreleases/grove-template-kilocode-sh-"$VERSION".zip \
  .genreleases/grove-template-kilocode-ps-"$VERSION".zip \
  .genreleases/grove-template-auggie-sh-"$VERSION".zip \
  .genreleases/grove-template-auggie-ps-"$VERSION".zip \
  .genreleases/grove-template-roo-sh-"$VERSION".zip \
  .genreleases/grove-template-roo-ps-"$VERSION".zip \
  .genreleases/grove-template-codebuddy-sh-"$VERSION".zip \
  .genreleases/grove-template-codebuddy-ps-"$VERSION".zip \
  .genreleases/grove-template-qoder-sh-"$VERSION".zip \
  .genreleases/grove-template-qoder-ps-"$VERSION".zip \
  .genreleases/grove-template-amp-sh-"$VERSION".zip \
  .genreleases/grove-template-amp-ps-"$VERSION".zip \
  .genreleases/grove-template-shai-sh-"$VERSION".zip \
  .genreleases/grove-template-shai-ps-"$VERSION".zip \
  .genreleases/grove-template-q-sh-"$VERSION".zip \
  .genreleases/grove-template-q-ps-"$VERSION".zip \
  .genreleases/grove-template-bob-sh-"$VERSION".zip \
  .genreleases/grove-template-bob-ps-"$VERSION".zip \
  --title "Grove Templates - $VERSION_NO_V" \
  --notes-file release_notes.md
