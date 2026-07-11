from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RootConfigDTO:
    project: Path
    registry: Path
    workspace: Path
