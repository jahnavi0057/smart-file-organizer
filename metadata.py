from pathlib import Path
from datetime import datetime


def show_metadata(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print("Folder does not exist.")
        return

    print("\nFILE METADATA")
    print("-" * 60)

    for file in folder.rglob("*"):
        if not file.is_file():
            continue

        size = file.stat().st_size
        modified = datetime.fromtimestamp(
            file.stat().st_mtime
        ).strftime("%Y-%m-%d %H:%M:%S")

        print(f"File Name : {file.name}")
        print(f"Size      : {size} bytes")
        print(f"Type      : {file.suffix or 'No extension'}")
        print(f"Modified  : {modified}")
        print("-" * 60)


if __name__ == "__main__":
    folder_path = input("Enter folder path: ")
    show_metadata(folder_path)
