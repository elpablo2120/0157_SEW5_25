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

    # Eine Kante mithilfe von Knotenindizes erzeugen und hinzufügen (Hilfsmethode)
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)

    def add_edge_by_indices(self, u: int, v: int, w: float = 1) -> Edge:
        edge = Edge(u, v, w)
        self.add_edge(edge)
        return edge

    def add_edge_by_vertices(self, first: V, second: V, w: float = 1) -> Edge:
        u, v = self._vertices.index(first), self._vertices.index(second)
        return self.add_edge_by_indices(u, v, w)


if __name__ == "__main__":
    # Test des Graphen
    print("Erstelle neuen Graphen...")
    graph = Graph[str]()

    print(f"Anzahl Knoten vor dem Hinzufügen: {graph.vertex_count}")

    print("Füge Knoten 'A' hinzu...")
    index_a = graph.add_vertex('A')
    print(f"Knoten 'A' wurde an Index {index_a} hinzugefügt.")

    print("Füge Knoten 'B' hinzu...")
    index_b = graph.add_vertex('B')
    print(f"Knoten 'B' wurde an Index {index_b} hinzugefügt.")



    print("-----------------------------------------------------")

    print("Füge Kante von 'A' nach 'B' hinzu...")
    graph.add_edge(Edge(1, 2, 1))

    print("Füge Kante von 'B' nach 'A' mit Index hinzu...")
    graph.add_edge_by_indices(1, 0, 2)

    print("Füge Kante von 'A' nach 'B' mit Knoten hinzu...")
    graph.add_edge_by_vertices('A', 'B', 3)

    print("-----------------------------------------------------")

    print(f"Aktuelle Anzahl Knoten: {graph.vertex_count}")
    print(f"Aktuelle Anzahl Kanten: {graph.edge_count}")

    print("-----------------------------------------------------")

    #Print all edges
    for i, edges in enumerate(graph._edges):
        for edge in edges:
            print(f"Kante: {edge}")

    print("-----------------------------------------------------")

    #print all vertices
    for i, vertex in enumerate(graph._vertices):
        print(f"Vertex: {vertex}")

    print("-----------------------------------------------------")










# def add_edge(self, edge: Edge) -> None:  # Eine Kante mithilfe von Knotenindizes erzeugen und hinzufügen (Hilfsmethode)
# def add_edge_by_indices(self, u: int, v: int, w=1) -> Edge:  # Eine Kante durch Nachschlagen von Knotenindizes hinzufügen (Hilfsmethode)
# def add_edge_by_vertices(self, first: V, second: V, w:float = 1) -> Edge:

# #Ein Graph G = (V, E, w) besteht aus
# #1. einer Menge V von Knoten (vertex)
# #2. einer Menge E von Kanten (edge) zwischen einigen der Knoten
# #3. (einer Gewichtsfunktion)