# from model.joint2D import Joint2D
from typing import NamedTuple

class Joint(NamedTuple):
    x: float
    y: float
    z: float
    name: str