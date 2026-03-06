
import pytest
from pathlib import Path
from organizer.organizer import FileOrganizer


def make_organizer(tmp_path: Path) -> FileOrganizer:
    """Helper that creates a FileOrganizer pointed at a temp directory."""
    return FileOrganizer(str(tmp_path))


def test_scan_files(tmp_path: Path) -> None:
    """Scanner finds the correct number of files."""
    (tmp_path / "file1.jpg").touch()
    (tmp_path / "file2.pdf").touch()
    (tmp_path / "file3.py").touch()

    organizer = make_organizer(tmp_path)
    files = organizer.scan_files()

    assert len(files) == 3


def test_categorize_image(tmp_path: Path) -> None:
    """Known image extensions return Images category."""
    organizer = make_organizer(tmp_path)
    result = organizer.categorize(Path("photo.jpg"))
    assert result == "Images"


def test_categorize_document(tmp_path: Path) -> None:
    """Known document extensions return Documents category."""
    organizer = make_organizer(tmp_path)
    result = organizer.categorize(Path("resume.pdf"))
    assert result == "Documents"


def test_categorize_unknown(tmp_path: Path) -> None:
    """Unknown extensions return Misc."""
    organizer = make_organizer(tmp_path)
    result = organizer.categorize(Path("weird_file.xyz"))
    assert result == "Misc"


def test_categorize_no_extension(tmp_path: Path) -> None:
    """Files with no extension return Misc."""
    organizer = make_organizer(tmp_path)
    result = organizer.categorize(Path("README"))
    assert result == "Misc"


def test_create_folder(tmp_path: Path) -> None:
    """Folder gets physically created on disk."""
    organizer = make_organizer(tmp_path)
    folder = organizer.create_folder("Images")

    assert folder.exists()
    assert folder.is_dir()
    assert folder.name == "Images"


def test_create_folder_already_exists(tmp_path: Path) -> None:
    """Creating a folder that already exists does not crash."""
    organizer = make_organizer(tmp_path)
    organizer.create_folder("Images")
    organizer.create_folder("Images")  # second call should not raise


def test_move_file(tmp_path: Path) -> None:
    """File moves to correct destination folder."""
    source = tmp_path / "photo.jpg"
    source.touch()

    destination = tmp_path / "Images"
    destination.mkdir()

    organizer = make_organizer(tmp_path)
    result = organizer.move_file(source, destination)

    assert (destination / "photo.jpg").exists()
    assert not source.exists()
    assert "MOVED" in result


def test_move_file_already_exists(tmp_path: Path) -> None:
    """File is skipped if it already exists at destination."""
    source = tmp_path / "photo.jpg"
    source.touch()

    destination = tmp_path / "Images"
    destination.mkdir()
    (destination / "photo.jpg").touch()

    organizer = make_organizer(tmp_path)
    result = organizer.move_file(source, destination)

    assert "SKIPPED" in result


def test_organize_full_pipeline(tmp_path: Path) -> None:
    """Full pipeline moves all files into correct folders."""
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "resume.pdf").touch()
    (tmp_path / "script.py").touch()

    organizer = make_organizer(tmp_path)
    organizer.organize()

    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "Documents" / "resume.pdf").exists()
    assert (tmp_path / "Code" / "script.py").exists()