"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "0.1"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "In Progress"
"""
from dataclasses import dataclass

@dataclass
class Edge:
    """
    Eine Kante in einem gewichteten Graphen.
    u und v sind die Indizes der Knoten, die die Kante verbindet (u=von, v=nach);
    w = Gewicht der Kante
    >>> e1 = Edge(1, 2, 99)
    >>> e1
    Edge(u=1, v=2, weight=99)
    >>> print(e1)
    1 --99-> 2
    """
    u: int
    v: int
    weight: int

    def __str__(self) -> str:
        return f"{self.u} --{self.weight}-> {self.v}"
