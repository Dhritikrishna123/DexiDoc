import os
import pytest
import shutil
from pathlib import Path
from src.discovery import FileScanner

@pytest.fixture
def scanner_test_dir(tmp_path):
    """Create a temporary directory structure for testing."""
    # Structure:
    # root/
    #   doc1.txt
    #   script.py (excluded ext)
    #   subdir/
    #     doc2.pdf
    #     ignore.txt (excluded name)
    #   ignored_folder/
    #     doc3.docx
    #   nested/
    #     deep/
    #       skip_me.txt (excluded relative)
    
    root = tmp_path / "scan_root"
    root.mkdir()
    
    (root / "doc1.txt").touch()
    (root / "script.py").touch()
    
    subdir = root / "subdir"
    subdir.mkdir()
    (subdir / "doc2.pdf").touch()
    (subdir / "ignore.txt").touch()
    
    ignored = root / "ignored_folder"
    ignored.mkdir()
    (ignored / "doc3.docx").touch()
    
    nested = root / "nested" / "deep"
    nested.mkdir(parents=True)
    (nested / "skip_me.txt").touch()
    
    return root

def test_scanner_basic(scanner_test_dir):
    extensions = [".txt", ".pdf"]
    excludes = []
    scanner = FileScanner(scanner_test_dir, excludes, extensions)
    
    results = list(scanner.scan())
    files = {f.path.name for f in results}
    
    assert "doc1.txt" in files
    assert "doc2.pdf" in files
    assert "script.py" not in files # Wrong extension

def test_scanner_exclusions(scanner_test_dir):
    extensions = [".txt", ".pdf", ".docx"]
    # Exclude by name and by relative path
    excludes = ["ignored_folder", "ignore.txt", "nested/deep/skip_me.txt"]
    scanner = FileScanner(scanner_test_dir, excludes, extensions)
    
    results = list(scanner.scan())
    paths = {str(f.path.relative_to(scanner_test_dir)).replace(os.sep, "/") for f in results}
    
    assert "doc1.txt" in paths
    assert "subdir/doc2.pdf" in paths
    
    # Excluded by dir name
    assert "ignored_folder/doc3.docx" not in paths
    # Excluded by file name
    assert "subdir/ignore.txt" not in paths
    # Excluded by relative path
    assert "nested/deep/skip_me.txt" not in paths

def test_scanner_invalid_path():
    with pytest.raises(FileNotFoundError):
        list(FileScanner(Path("non_existent_path")).scan())
        
    with pytest.raises(NotADirectoryError):
        # Point to a file, not a dir
        list(FileScanner(Path(__file__)).scan())
