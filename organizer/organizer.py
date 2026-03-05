from pathlib import Path
from typing import List, Set

from organizer.utils import get_logger, validate_directory
from organizer.rules import Extension_map


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
    def categorize(self, file: Path) -> str:
        extension = file.suffix.lower()

        for category,extensions in Extension_map.items():
            if extension in extensions:
                return category

        return "Misc"
    def create_folder(self, folder_name: str) -> Path:
        folder_path = self.directory / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"  Folder ready: {folder_name}/")
        return folder_path
    def organize(self) -> None:
        self.scan_files()
        if not self.files:
            logger.warning("NO files found. Nothing to organize")
            return
        categories_needed: Set[str] = set()
        
        for f in self.files:
            category = self.categorize(f)   
            categories_needed.add(category)
            logger.info(f"  Detected: {f.name} -> {category}")
        
        logger.info("Creating category folders...")

        for category in categories_needed:
            self.create_folder(category)