from pathlib import Path
from typing import List

from organizer.utils import get_logger, validate_directory

logger = get_logger(__name__)

class FileOrganizer:
    def __init__(self, path:str, workers: int = 4) -> None:
        self.directory: Path = validate_directory(path)
        self.workers: int = workers
        self.files: List[Path] = []
        
        logger.info(f"FileOrganizer Intialized -> {self.directory}")
    def scan_files(self) -> List[Path]:
        self.files = [
            item for item in self.directory.iterdir()
            if item.is_file()
        ]
        logger.info(f"Found {len(self.files)} file(s) to organize")
        return self.files
    def organize(self) -> None:
        self.scan_files()
        if not self.files:
            logger.warning("NO files found. Nothing to organize")
            return
        for f in self.files:
            logger.info(f"  Detected: {f.name}")