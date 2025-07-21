from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Part:
    name: str
    connections: Dict[str, str]