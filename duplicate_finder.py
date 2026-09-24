from pathlib import Path
import hashlib


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicates(folder_path):
    folder = Path(folder_path)
    hashes = {}

    for file in folder.rglob("*"):

        if not file.is_file():
            continue

        file_hash = calculate_hash(file)

        if file_hash in hashes:
            print("Duplicate found:")
            print("  Original :", hashes[file_hash])
            print("  Duplicate:", file)
            print()
        else:
            hashes[file_hash] = file


if __name__ == "__main__":
    folder_path = input("Enter folder path: ")
    find_duplicates(folder_path)