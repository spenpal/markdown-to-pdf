#!/usr/bin/env bash
set -euo pipefail

# Check if filename provided
if [ $# -eq 0 ]; then
    echo "Usage: docker run --rm -v \$(pwd):/data md2pdf FILENAME.md"
    echo "Example: docker run --rm -v \$(pwd):/data md2pdf document.md"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${INPUT_FILE%.*}.pdf"

pandoc --defaults=/config/defaults.yaml "/data/$INPUT_FILE" -o "/data/$OUTPUT_FILE"

echo "Converted: $INPUT_FILE --> $OUTPUT_FILE"
