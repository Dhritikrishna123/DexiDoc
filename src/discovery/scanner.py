import os
import fnmatch
from pathlib import Path
from typing import List, Generator, Set
from ..models import DiscoveredFile

class FileScanner:
    def __init__(self, base_path: Path, excludes: List[str] = None, extensions: List[str] = None):
        self.base_path = base_path
        self.excludes = excludes or []
        self.extensions = set(ext.lower() for ext in (extensions or []))

    def _is_excluded(self, path: Path) -> bool:
        """Check if path matches any exclude pattern."""
        name = path.name
        rel_path = None
        try:
            rel_path = path.relative_to(self.base_path).as_posix()
        except ValueError:
            pass

        for pattern in self.excludes:
            if fnmatch.fnmatch(name, pattern):
                return True
            if rel_path and fnmatch.fnmatch(rel_path, pattern):
                return True
        return False

    def _is_allowed_extension(self, path: Path) -> bool:
        """Check if file extension is in allowed list."""
        if not self.extensions:
            # If no extensions defined, strict filtering implies matching nothing.
            return False 
        return path.suffix.lower() in self.extensions

    def scan(self) -> Generator[DiscoveredFile, None, None]:
        """Recursive directory scan yielding DiscoveredFile objects."""
        # Validate base path
        if not self.base_path.exists():
            raise FileNotFoundError(f"Base path does not exist: {self.base_path}")

        if not self.base_path.is_dir():
            raise NotADirectoryError(f"Base path is not a directory: {self.base_path}")

        # Use os.walk for controlled traversal (pruning directories)
        for root, dirs, files in os.walk(self.base_path):
            root_path = Path(root)
            
            # Prune directories based on exclusion rules
            # We modify dirs in-place to stop os.walk from entering them
            dirs[:] = [d for d in dirs if not self._is_excluded(root_path / d)]
            
            for file in files:
                file_path = root_path / file
                
                if self._is_excluded(file_path):
                    continue
                
                if self._is_allowed_extension(file_path):
                    try:
                        size = file_path.stat().st_size
                        yield DiscoveredFile(
                            path=file_path,
                            file_type=file_path.suffix.lower(),
                            size=size
                        )
                    except OSError:
                        # Skip files we can't stat
                        continue
