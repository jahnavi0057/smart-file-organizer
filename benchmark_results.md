# Smart File Organizer - Performance Benchmark

## Objective

The objective of this benchmark is to compare the performance of sequential file processing with concurrent file processing using Python `ThreadPoolExecutor`.

The benchmark measures the execution time and throughput of the Smart File Organizer for different numbers of files.

## Test Environment

- Operating System: Ubuntu Linux on WSL2
- Programming Language: Python 3
- Python Version: 3.14
- Concurrent Workers: 4
- Storage: Local WSL-mounted filesystem
- Test workloads: 100, 500, and 1000 files

## Methodology

Two implementations were tested:

1. **Sequential Processing**
   - Files are processed one at a time.
   - Each file is categorized and moved before processing the next file.

2. **Concurrent Processing**
   - Files are processed using Python `ThreadPoolExecutor`.
   - Four worker threads are used to process file operations concurrently.

The execution time was measured using Python's `time.perf_counter()`.

Throughput was calculated as:

```text
Throughput = Number of Files / Execution Time
