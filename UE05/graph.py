"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "0.1"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "In Progress"
"""

from typing import TypeVar, Generic, List, Optional
from edge import Edge

V = TypeVar('V') # Typ der Knoten im Graphen

class Graph(Generic[V]):
    def __init__(self, vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices # Liste aller Knoten des Graphen
        self._edges: List[List[Edge]] = [[] for _ in vertices]

