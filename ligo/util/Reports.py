from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class ReportOutput:
    def __init__(self, path: Path, name: str = None):
        self.path = Path(path)
        self.name = name


@dataclass
class ReportResult:
    name: str = None
    info: str = None  # optional extra info about this report to display to the user
    output_figures: List[ReportOutput] = field(default_factory=lambda: [])
    output_tables: List[ReportOutput] = field(default_factory=lambda: [])
    output_text: List[ReportOutput] = field(default_factory=lambda: [])
