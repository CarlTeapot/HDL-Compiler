from dataclasses import dataclass
from typing import Dict

@dataclass
class Part:
    name: str
    connections: Dict[str, str]