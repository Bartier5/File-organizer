import os
import logging
from pathlib import Path

def get_logger(name:str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt="[%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
def validate_directory(path: str) -> Path:
    resolved = Path(path).resolve()
    if not resolved.exists():
        raise NotADirectoryError(f"Path does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {resolved}")
    if not os.access(resolved, os.R_OK):
        raise PermissionError(f"Directory is not readable: {resolved}")

    return resolved

        