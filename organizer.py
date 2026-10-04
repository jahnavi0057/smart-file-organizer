from pathlib import Path
import shutil
import logging
from recovery import record_move


CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Archives": [".zip", ".rar", ".7z"]
}


logging.basicConfig(
    filename="/mnt/d/smart-file-organizer/logs/organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def get_category(extension):
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def organize_folder(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("Folder does not exist.")
        return

    for file in folder.iterdir():

        if not file.is_file():
            continue

        category = get_category(file.suffix.lower())

        category_folder = folder / category
        category_folder.mkdir(exist_ok=True)

        destination = category_folder / file.name

        counter = 1

        while destination.exists():
            destination = category_folder / f"{file.stem}_{counter}{file.suffix}"
            counter += 1

        try:
            shutil.move(str(file), str(destination))

            # Record the movement for recovery/undo
            record_move(file, destination)

            logging.info(
                f"Moved: {file} -> {destination}"
            )

            print(f"Moved: {file.name} -> {category}/")

        except Exception as error:

            logging.error(
                f"Failed to move {file}: {error}"
            )

            print(
                f"Error moving {file.name}: {error}"
            )

    print("File organization completed!")


if __name__ == "__main__":

    print("Smart File Organizer")
    print("--------------------")

    folder_path = input("Enter folder path: ")

    organize_folder(folder_path)
