from dataclasses import dataclass

@dataclass
class Label:
    name: str
    x: float
    y: float

@dataclass
class Wire:
    x1: float
    y1: float
    x2: float
    y2: float
