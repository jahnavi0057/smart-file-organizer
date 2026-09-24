#!/bin/bash

PROJECT="/mnt/d/smart-file-organizer"
ORGANIZER="$PROJECT/organizer.py"
FOLDER="/mnt/d/organizer-demo"

echo "Starting Smart File Organizer..."

echo "$FOLDER" | python3 "$ORGANIZER"

if [ $? -eq 0 ]; then
    echo "Organization completed successfully."
else
    echo "Organization failed."
fi