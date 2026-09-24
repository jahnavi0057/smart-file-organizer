from pathlib import Path
import shutil
import time
from concurrent.futures import ThreadPoolExecutor


CATEGORIES = {
    "Documents": [".txt", ".pdf", ".doc", ".docx", ".csv"],
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
    destination_folder = folder / category
    destination_folder.mkdir(exist_ok=True)

    destination = destination_folder / file.name

    counter = 1
    while destination.exists():
        destination = destination_folder / f"{file.stem}_{counter}{file.suffix}"
        counter += 1

    shutil.move(str(file), str(destination))


def sequential_organize(folder):
    files = [f for f in folder.iterdir() if f.is_file()]

    start = time.perf_counter()

    for file in files:
        move_file(file, folder)

    return time.perf_counter() - start


def concurrent_organize(folder):
    files = [f for f in folder.iterdir() if f.is_file()]

    start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda f: move_file(f, folder), files)

    return time.perf_counter() - start


def create_test_files(folder, count):
    folder.mkdir(parents=True, exist_ok=True)

    for i in range(count):
        file = folder / f"test_{i}.txt"
        file.write_text(f"Test data {i}")


def reset_folder(folder):
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True)


def run_benchmark(count):
    sequential_folder = Path(f"/mnt/d/benchmark-sequential-{count}")
    concurrent_folder = Path(f"/mnt/d/benchmark-concurrent-{count}")

    reset_folder(sequential_folder)
    reset_folder(concurrent_folder)

    create_test_files(sequential_folder, count)

    for file in sequential_folder.iterdir():
        shutil.copy(file, concurrent_folder / file.name)

    sequential_time = sequential_organize(sequential_folder)
    concurrent_time = concurrent_organize(concurrent_folder)

    sequential_speed = count / sequential_time
    concurrent_speed = count / concurrent_time

    print(f"\n--- {count} FILES ---")
    print(f"Sequential Time : {sequential_time:.4f} seconds")
    print(f"Concurrent Time : {concurrent_time:.4f} seconds")
    print(f"Sequential Speed: {sequential_speed:.2f} files/sec")
    print(f"Concurrent Speed: {concurrent_speed:.2f} files/sec")


if __name__ == "__main__":
    print("SMART FILE ORGANIZER - PERFORMANCE BENCHMARK")

    for count in [100, 500, 1000]:
        run_benchmark(count)
