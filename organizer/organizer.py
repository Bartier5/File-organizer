from pathlib import Path
from typing import List

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
    def move_file(self, file: Path, destination: Path) -> str:
        target = destination / file.name
        if target.exists():
            result = f"  SKIPPED: {file.name} already exists in {destination.name}/"
            logger.warning(result)
            return result
        file.rename(target)
        result = f"  MOVED: {file.name} → {destination.name}/"
        logger.info(result)
        return result
    def organize(self) -> None:
        self.scan_files()
        if not self.files:
            logger.warning("NO files found. Nothing to organize")
            return
        logger.info("Creating category folders...")
        
        for f in self.files:
            category = self.categorize(f)   
            destination = self.create_folder(category)
            self.move_file(f, destination)
            logger.info("Organization complete.")

     