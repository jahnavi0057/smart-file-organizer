from pathlib import Path
import json
import shutil

HISTORY_FILE = Path("/mnt/d/smart-file-organizer/logs/move_history.json")


def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_history(history):
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def record_move(source, destination):
    history = load_history()

    history.append({
        "source": str(source),
        "destination": str(destination)
    })

    save_history(history)


def undo_last_move():
    history = load_history()

    if not history:
        print("No file movement available to undo.")
        return

    last_move = history[-1]

    source = Path(last_move["source"])
    destination = Path(last_move["destination"])

    if not destination.exists():
        print("Moved file no longer exists.")
        return

    source.parent.mkdir(parents=True, exist_ok=True)

    if source.exists():
        print("Original location already contains a file.")
        return

    shutil.move(str(destination), str(source))

    history.pop()
    save_history(history)

    print(f"Undo successful: {destination.name}")
    print(f"Restored to: {source}")


def show_history():
    history = load_history()

    if not history:
        print("No movement history.")
        return

    print("\nFILE MOVEMENT HISTORY")
    print("-" * 60)

    for i, move in enumerate(history, start=1):
        print(f"{i}.")
        print(f"   From: {move['source']}")
        print(f"   To  : {move['destination']}")


if __name__ == "__main__":

    print("\nSmart File Organizer - Recovery System")
    print("1. Show history")
    print("2. Undo last move")

    choice = input("Enter choice: ")

    if choice == "1":
        show_history()

    elif choice == "2":
        undo_last_move()

    else:
        print("Invalid choice.")
