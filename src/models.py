from dataclasses import dataclass
from pathlib import Path

@dataclass
class DiscoveredFile:
    path: Path
    file_type: str
    size: int
