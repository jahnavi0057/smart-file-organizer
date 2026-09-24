from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor
import time


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
    extension = file.suffix.lower()
    category = get_category(extension)

    category_folder = folder / category
    category_folder.mkdir(exist_ok=True)

    destination = category_folder / file.name

    counter = 1
    while destination.exists():
        destination = category_folder / f"{file.stem}_{counter}{file.suffix}"
        counter += 1

    shutil.move(str(file), str(destination))

    return file.name, category


def organize_concurrently(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("Folder does not exist.")
        return

    files = [file for file in folder.iterdir() if file.is_file()]

    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(
            lambda file: move_file(file, folder),
            files
        )

        for filename, category in results:
            print(f"Moved: {filename} -> {category}/")

    end_time = time.perf_counter()

    print("\nConcurrent organization completed!")
    print(f"Files processed: {len(files)}")
    print(f"Execution time: {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    folder_path = input("Enter folder path: ")
    organize_concurrently(folder_path)
