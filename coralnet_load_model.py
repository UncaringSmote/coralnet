from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class Point:
    row:int
    column:int

@dataclass_json
@dataclass
class Attributes:
    url:str
    points:List[Point]
@dataclass_json
@dataclass
class Data:
    attributes:Attributes
    type: str = 'image'

@dataclass_json
@dataclass
class CoralnetLoadModel:
    data:[Data]
