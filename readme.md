# File Organizer

A command-line tool that automatically sorts files into categorized folders based on their file extension. Built with clean architecture and multithreading for concurrent file operations.

---

## What It Does

Point it at any folder on your machine and it will:

- Scan all files in that directory
- Identify each file's type by extension
- Create category folders automatically
- Move every file into the correct folder concurrently

---

## Project Structure
```
file_organizer/
│
├── main.py                  # CLI entry point
├── organizer/
│   ├── __init__.py
│   ├── organizer.py         # Core logic and FileOrganizer class
│   ├── rules.py             # Extension to category mapping
│   └── utils.py             # Logging and path validation
│
├── tests/
│   └── test_basic.py        # Full test suite
│
├── conftest.py              # Pytest configuration
└── README.md
```

---

## Getting Started

**Clone the repository**
```bash
git clone https://github.com/Bartier5/file-organizer.git
cd file-organizer
```

**Run the organizer**
```bash
python main.py
```

When prompted, enter the full path to the folder you want to organize:
```
========================================
   File Organizer — Portfolio v1
========================================

Enter the directory path to organize:
> C:\Users\yourname\Desktop\messy_folder
```

---

## Example Output
```
[INFO] FileOrganizer initialized → C:\Users\yourname\Desktop\messy_folder
[INFO] Found 6 file(s) to organize.
[INFO] Moving 6 file(s) using 4 workers...
[INFO]   MOVED: resume.pdf → Documents/
[INFO]   MOVED: photo.jpg → Images/
[INFO]   MOVED: budget.xlsx → Documents/
[INFO]   MOVED: intro.mp4 → Videos/
[INFO]   MOVED: script.py → Code/
[INFO]   MOVED: song.mp3 → Audio/
[INFO] Organization complete.
```

---

## Supported Categories

| Category | Extensions |
|---|---|
| Images | .jpg .jpeg .png .gif .bmp .svg .webp |
| Documents | .pdf .docx .doc .txt .xlsx .pptx .csv |
| Videos | .mp4 .mov .avi .mkv .flv .wmv |
| Audio | .mp3 .wav .aac .flac .ogg |
| Code | .py .js .ts .html .css .json .xml |
| Archives | .zip .rar .tar .gz .7z |
| Misc | anything else |

---

## Adding New Categories

Open `organizer/rules.py` and add a new entry to `EXTENSION_MAP`:
```python
"Design": [".fig", ".xd", ".sketch"],
```

No other file needs to change. The folder will be created and used automatically on the next run.

---

## Running Tests
```bash
pip install pytest
pytest tests/ -v
```

Expected output:
```
tests/test_basic.py::test_scan_files                    PASSED
tests/test_basic.py::test_categorize_image              PASSED
tests/test_basic.py::test_categorize_document           PASSED
tests/test_basic.py::test_categorize_unknown            PASSED
tests/test_basic.py::test_categorize_no_extension       PASSED
tests/test_basic.py::test_create_folder                 PASSED
tests/test_basic.py::test_create_folder_already_exists  PASSED
tests/test_basic.py::test_move_file                     PASSED
tests/test_basic.py::test_move_file_already_exists      PASSED
tests/test_basic.py::test_organize_full_pipeline        PASSED

10 passed
```

---

## Built With

- Python 3.14
- pathlib — file system handling
- concurrent.futures — multithreaded file movement
- logging — structured console output
- pytest — test suite

---

## Notes

- Non-recursive — only organizes files in the top level of the provided directory
- Files with unrecognized extensions go into a `Misc` folder
- If a file with the same name already exists at the destination it is skipped, not overwritten
- Thread pool size defaults to 4 workers, configurable via the `workers` parameter