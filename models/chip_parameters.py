from dataclasses import dataclass, field
from typing import List

from models.part import Part


@dataclass
class ChipParameters:
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    parts: List['Part'] = field(default_factory=list)