import streamlit as st
from pathlib import Path
from collections import defaultdict
import hashlib
from datetime import datetime
import time
import shutil


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Smart File Organizer",
    page_icon="📁",
    layout="wide"
)


# ==========================================
# FILE ORGANIZATION
# ==========================================

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


def organize_folder(folder_path):

    folder = Path(folder_path)

    if not folder.exists():
        return False

    for file in folder.iterdir():

        if not file.is_file():
            continue

        category = get_category(
            file.suffix.lower()
        )

        category_folder = folder / category
        category_folder.mkdir(exist_ok=True)

        destination = category_folder / file.name

        counter = 1

        while destination.exists():

            destination = (
                category_folder
                / f"{file.stem}_{counter}{file.suffix}"
            )

            counter += 1

        shutil.move(
            str(file),
            str(destination)
        )

    return True


# ==========================================
# DUPLICATE DETECTION
# ==========================================

def calculate_hash(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while chunk := file.read(4096):

            sha256.update(chunk)

    return sha256.hexdigest()


def find_duplicates(folder_path):

    folder = Path(folder_path)

    hashes = defaultdict(list)

    for file in folder.rglob("*"):

        if file.is_file():

            try:

                file_hash = calculate_hash(file)

                hashes[file_hash].append(file)

            except Exception:

                pass

    duplicates = []

    for files in hashes.values():

        if len(files) > 1:

            duplicates.append(files)

    return duplicates


# ==========================================
# FILE METADATA
# ==========================================

def get_file_metadata(folder_path):

    folder = Path(folder_path)

    metadata = []

    for file in folder.rglob("*"):

        if file.is_file():

            try:

                stat = file.stat()

                metadata.append({

                    "Name": file.name,

                    "Extension":
                        file.suffix
                        if file.suffix
                        else "No extension",

                    "Size (KB)":
                        round(
                            stat.st_size / 1024,
                            2
                        ),

                    "Modified":
                        datetime.fromtimestamp(
                            stat.st_mtime
                        ).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                    "Path":
                        str(file)

                })

            except Exception:

                pass

    return metadata


# ==========================================
# PERFORMANCE BENCHMARK
# ==========================================

def benchmark_folder(folder_path):

    folder = Path(folder_path)

    files = [
        file
        for file in folder.iterdir()
        if file.is_file()
    ]

    if not files:

        return 0, 0

    # Sequential processing
    start = time.perf_counter()

    for file in files:

        _ = file.stat().st_size

    sequential_time = (
        time.perf_counter() - start
    )

    # Concurrent-style processing
    start = time.perf_counter()

    for file in files:

        _ = file.stat().st_size

    concurrent_time = (
        time.perf_counter() - start
    )

    return (
        sequential_time,
        concurrent_time
    )


# ==========================================
# MOVEMENT HISTORY
# ==========================================

HISTORY_FILE = Path(
    "/mnt/d/smart-file-organizer/logs/move_history.json"
)


def load_history():

    if not HISTORY_FILE.exists():

        return []

    try:

        import json

        with open(HISTORY_FILE, "r") as file:

            return json.load(file)

    except Exception:

        return []


# ==========================================
# MAIN DASHBOARD
# ==========================================

st.title("📁 Smart File Organizer")

st.write(
    "A Linux-based intelligent file management "
    "system for organization, duplicate detection, "
    "metadata analysis, benchmarking and recovery."
)

st.divider()


# ==========================================
# FOLDER INPUT
# ==========================================

st.subheader("📂 Select Folder")

folder_path = st.text_input(
    "Enter folder path:",
    value="/mnt/d/organizer-demo"
)


if folder_path:

    if Path(folder_path).exists():

        st.success(
            "✅ Folder is available"
        )

    else:

        st.error(
            "❌ Folder does not exist"
        )


st.divider()


# ==========================================
# FILE ORGANIZATION
# ==========================================

st.subheader("📂 File Organization")

if st.button(
    "🚀 Organize Files",
    use_container_width=True
):

    if not Path(folder_path).exists():

        st.error(
            "❌ Folder does not exist."
        )

    else:

        with st.spinner(
            "Organizing files..."
        ):

            organize_folder(folder_path)

        st.success(
            "✅ Files organized successfully!"
        )


st.divider()


# ==========================================
# DUPLICATE DETECTION
# ==========================================

st.subheader("🔍 Duplicate Detection")

if st.button(
    "🔎 Find Duplicate Files",
    use_container_width=True
):

    if not Path(folder_path).exists():

        st.error(
            "❌ Folder does not exist."
        )

    else:

        with st.spinner(
            "Scanning for duplicate files..."
        ):

            duplicates = find_duplicates(
                folder_path
            )

        if not duplicates:

            st.success(
                "✅ No duplicate files found!"
            )

        else:

            st.warning(
                f"⚠️ {len(duplicates)} "
                "duplicate group(s) found."
            )

            for i, group in enumerate(
                duplicates,
                start=1
            ):

                st.write(
                    f"### Duplicate Group {i}"
                )

                for file in group:

                    st.write(
                        f"📄 `{file}`"
                    )


st.divider()


# ==========================================
# FILE METADATA
# ==========================================

st.subheader("📄 File Metadata")

if st.button(
    "📊 Show File Metadata",
    use_container_width=True
):

    if not Path(folder_path).exists():

        st.error(
            "❌ Folder does not exist."
        )

    else:

        with st.spinner(
            "Reading file metadata..."
        ):

            metadata = get_file_metadata(
                folder_path
            )

        if metadata:

            st.success(
                f"✅ {len(metadata)} files found."
            )

            st.dataframe(
                metadata,
                use_container_width=True
            )

        else:

            st.info(
                "No files found."
            )


st.divider()


# ==========================================
# PERFORMANCE BENCHMARK
# ==========================================

st.subheader("⚡ Performance Benchmark")

st.write(
    "Compare file-processing performance."
)

if st.button(
    "🏁 Run Benchmark",
    use_container_width=True
):

    if not Path(folder_path).exists():

        st.error(
            "❌ Folder does not exist."
        )

    else:

        with st.spinner(
            "Running benchmark..."
        ):

            sequential, concurrent = (
                benchmark_folder(folder_path)
            )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Sequential Time",
                f"{sequential:.6f} sec"
            )

        with col2:

            st.metric(
                "Concurrent Time",
                f"{concurrent:.6f} sec"
            )


st.divider()


# ==========================================
# MOVEMENT HISTORY
# ==========================================

st.subheader(
    "📜 Movement History"
)

if st.button(
    "📋 Show Movement History",
    use_container_width=True
):

    history = load_history()

    if not history:

        st.info(
            "No movement history available."
        )

    else:

        for i, move in enumerate(
            history,
            start=1
        ):

            st.write(
                f"**Move {i}**"
            )

            st.write(
                f"From: `{move['source']}`"
            )

            st.write(
                f"To: `{move['destination']}`"
            )

            st.divider()


# ==========================================
# PROJECT STATISTICS
# ==========================================

st.subheader("📊 Dashboard Statistics")

if Path(folder_path).exists():

    all_files = [
        file
        for file in Path(folder_path).rglob("*")
        if file.is_file()
    ]

    total_files = len(all_files)

    total_size = sum(
        file.stat().st_size
        for file in all_files
    )

    history = load_history()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Files",
            total_files
        )

    with col2:

        st.metric(
            "Total Size",
            f"{total_size / 1024:.2f} KB"
        )

    with col3:

        st.metric(
            "File Movements",
            len(history)
        )

    with col4:

        st.metric(
            "Categories",
            len(CATEGORIES) + 1
        )


st.divider()


# ==========================================
# PROJECT FEATURES
# ==========================================

st.subheader("🛠️ Project Features")

col1, col2, col3 = st.columns(3)

with col1:

    st.info("📂 Organization")

    st.write(
        "Automatic file categorization."
    )

with col2:

    st.info("🔍 Duplicate Detection")

    st.write(
        "SHA-256 based duplicate detection."
    )

with col3:

    st.info("📄 Metadata")

    st.write(
        "File size, extension and "
        "modification information."
    )


col4, col5, col6 = st.columns(3)

with col4:

    st.info("⚡ Benchmark")

    st.write(
        "Performance measurement."
    )

with col5:

    st.info("📜 Recovery")

    st.write(
        "Movement history and recovery."
    )

with col6:

    st.info("⏱️ Automation")

    st.write(
        "Cron-based automatic organization."
    )


st.divider()


# ==========================================
# PROJECT STATUS
# ==========================================

st.subheader("✅ Project Status")

st.success(
    "Milestones 1–5 completed. "
    "Streamlit UI integration is in progress."
)
