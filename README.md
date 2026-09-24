# Smart File Organizer for Linux

## Project Overview

Smart File Organizer is a Linux-based Python application that automatically organizes files into different folders based on their file types.

It is designed to reduce clutter in directories such as Downloads by automatically categorizing documents, images, videos, audio files, and archives.

## Features

- Automatic file organization
- File extension detection
- Automatic category folder creation
- Duplicate file detection using SHA-256 hashing
- Safe filename handling to prevent overwriting
- Activity logging
- File metadata analysis
- Linux shell script automation
- Cron-based scheduled execution

## File Categories

| Category | File Types |
|----------|------------|
| Documents | PDF, DOC, DOCX, TXT, CSV |
| Images | JPG, JPEG, PNG, GIF |
| Videos | MP4, MKV, AVI, MOV |
| Audio | MP3, WAV, FLAC |
| Archives | ZIP, RAR, 7Z |
| Others | Unsupported file types |

## Technologies Used

- Python 3
- Linux / Ubuntu
- WSL2
- Bash Shell
- Cron
- SHA-256
- Git and GitHub

## Project Structure

```text
smart-file-organizer/
├── organizer.py
├── duplicate_finder.py
├── metadata.py
├── run_organizer.sh
├── logs/
│   ├── organizer.log
│   └── cron.log
├── organizer_backup.py
├── duplicate_finder_backup.py
└── README.md
