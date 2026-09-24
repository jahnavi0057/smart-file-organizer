from pathlib import Path
import time
import shutil

CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".7z"]
}


def get_category(extension):
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def move_file(file, folder):
    category = get_category(file.suffix.lower())

    category_folder = folder / category
    category_folder.mkdir(exist_ok=True)

    destination = category_folder / file.name

    counter = 1
    while destination.exists():
        destination = category_folder / f"{file.stem}_{counter}{file.suffix}"
        counter += 1

    shutil.move(str(file), str(destination))

    print(f"Moved: {file.name} -> {category}/")


def monitor_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("Folder does not exist.")
        return

    processed_files = set()

    print(f"Monitoring: {folder}")
    print("Checking for new files...")
    print("Press Ctrl+C to stop.")

    try:
        while True:

            current_files = {
                file for file in folder.iterdir()
                if file.is_file()
            }

            new_files = current_files - processed_files

            for file in new_files:
                print(f"\nNew file detected: {file.name}")
                move_file(file, folder)

            processed_files.update(new_files)

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nFile monitor stopped.")


if __name__ == "__main__":
    folder_path = input("Enter folder to monitor: ")
    monitor_folder(folder_path)
