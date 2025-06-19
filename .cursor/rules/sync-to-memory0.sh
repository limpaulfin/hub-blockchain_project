#!/bin/bash

# ---
# title: Sync Project Memory to Memory Hub
# description: This script synchronizes the .memory/ directory of the current project to a central memory hub in OneDrive.
# author: Asi
# created: 2024-06-05
# ---

set -e # Exit immediately if a command exits with a non-zero status.

# Get the directory of the script itself.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Determine the project root directory (two levels up from the script's location).
PROJECT_ROOT=$(dirname "$(dirname "$SCRIPT_DIR")")
PROJECT_NAME=$(basename "$PROJECT_ROOT")

# Define the source directory. Note the trailing slash to copy contents.
SOURCE_DIR="$PROJECT_ROOT/.memory/"

# Check if the source directory exists.
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Source directory not found: $SOURCE_DIR"
    exit 1
fi

# Find the Memory Hub directory.
MEM_HUB=""
if [ -d "/home/fong/onedrive/memory0" ]; then
    MEM_HUB="/home/fong/onedrive/memory0"
elif [ -d "/home/fong/OneDrive/memory0" ]; then
    MEM_HUB="/home/fong/OneDrive/memory0"
else
    echo "Error: Memory hub directory not found."
    echo "Checked paths: /home/fong/onedrive/memory0 and /home/fong/OneDrive/memory0"
    exit 1
fi

# Define the destination directory.
DEST_DIR="$MEM_HUB/$PROJECT_NAME/.memory/"

# Create the destination directory if it doesn't exist.
echo "Ensuring destination directory exists: $DEST_DIR"
mkdir -p "$DEST_DIR"

# Perform the synchronization using rsync.
# -a: archive mode (preserves permissions, timestamps, etc.)
# -v: verbose output
# -h: human-readable numbers
# --delete: delete extraneous files from the destination
# --exclude: exclude specified files/directories
echo "Syncing from $SOURCE_DIR to $DEST_DIR"
rsync -avh --delete --exclude='.history' "$SOURCE_DIR" "$DEST_DIR"

echo "✅ Synchronization complete." 