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

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)

    @property
    def edge_count(self) -> int:
        return sum(len(edges) for edges in self._edges)

    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([])
        return len(self._vertices) - 1

# def add_edge(self, edge: Edge) -> None:  # Eine Kante mithilfe von Knotenindizes erzeugen und hinzufügen (Hilfsmethode)

if __name__ == "__main__":
    # Test des Graphen
    print("Erstelle neuen Graphen...")
    graph = Graph[str](["A"])

    print(f"Anzahl Knoten vor dem Hinzufügen: {graph.vertex_count}")

    print("Füge Knoten 'A' hinzu...")
    index_a = graph.add_vertex('A')
    print(f"Knoten 'A' wurde an Index {index_a} hinzugefügt.")

    print("Füge Knoten 'B' hinzu...")
    index_b = graph.add_vertex('B')
    print(f"Knoten 'B' wurde an Index {index_b} hinzugefügt.")

    print(f"Aktuelle Anzahl Knoten: {graph.vertex_count}")
    print(f"Aktuelle Anzahl Kanten: {graph.edge_count}")


# def add_edge(self, edge: Edge) -> None:  # Eine Kante mithilfe von Knotenindizes erzeugen und hinzufügen (Hilfsmethode)
# def add_edge_by_indices(self, u: int, v: int, w=1) -> Edge:  # Eine Kante durch Nachschlagen von Knotenindizes hinzufügen (Hilfsmethode)
# def add_edge_by_vertices(self, first: V, second: V, w:float = 1) -> Edge:

# #Ein Graph G = (V, E, w) besteht aus
# #1. einer Menge V von Knoten (vertex)
# #2. einer Menge E von Kanten (edge) zwischen einigen der Knoten
# #3. (einer Gewichtsfunktion)