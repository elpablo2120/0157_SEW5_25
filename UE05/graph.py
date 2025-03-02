"""
__author__ = "Paul Waldecker"
__email__ = "0157@htl.rennweg.at"
__version__ = "0.1"
__copyright__ = "Copyright 2024"
__license__ = "GPL"
__status__ = "In Progress"
"""

from typing import TypeVar, Generic, List, Optional, Tuple
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

    # Suche Knoten mit gegebenem Index
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    # Suche Index des gegebenen Knotens im Graphen
    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    # Bestimme die benachbarte Knoten des Knotens mit dem gegebenen Index
    # Rückgabewert ist eine Liste mit Tupeln.
    # Letzere bestehen aus den benachbarten Knoten und den Kantengewichtungen.
    def neighbors_for_index_with_weights(self, index: int) -> List[Tuple[V, float]]:
        return [(self.vertex_at(edge.v), edge.weight) for edge in self._edges[index]]

    # Bestimme alle Kanten, die mit einem Knoten am gegebenen Index verknüpft sind
    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]

    def edge_list_to_string(self, edge_list: List['Edge'], showWeights: bool = False) -> str:
        """
        Hilfsmethode, um einen Pfad (=Liste von Kanten) in eine Zeichenkette umzuwandeln.

        :param edge_list: Liste von Kanten
        :param showWeights: True, wenn die Gewichte der Kanten angezeigt werden sollen
        :return: zusammenhängende Zeichenkette, die die Kanten repräsentiert (getrennt durch "-->")

        >>> g = Graph(list("ABCDEFGH"))
        >>> e1 = g.add_edge_by_vertices("A", "B", 1)
        >>> e2 = g.add_edge_by_vertices("B", "C", 5)
        >>> e3 = g.add_edge_by_vertices("C", "D", 9)
        >>> g.edge_list_to_string([e1, e2, e3])
        'A-->B-->C-->D'
        >>> g.edge_list_to_string([e1, e2, e3], showWeights=True)
        'A-1->B-5->C-9->D'
        """
        if not edge_list:
            return ""

        path = [self.vertex_at(edge_list[0].u)]
        for edge in edge_list:
            if showWeights:
                path.append(f"-{edge.weight}->{self.vertex_at(edge.v)}")
            else:
                path.append(f"-->{self.vertex_at(edge.v)}")
        return "".join(path)

    def set_adjacency_matrix(self, lines: List[str]) -> None:
        # Entferne Leerzeichen und spalte die erste Zeile in Knotennamen
        headers = [col.strip() for col in lines[0].split(";")][1:]  # Skip the first empty element
        print(f"Headers: {headers}")

        # Überprüfen, ob die Kopfzeile eindeutige Knoten enthält
        if len(headers) != len(set(headers)):
            raise RuntimeError("Duplicated nodes in header row")

        self._vertices = headers
        self._edges = [[] for _ in headers]

        for row_index, line in enumerate(lines[1:]):
            cells = [cell.strip() for cell in line.split(";")]
            print(f"Line {row_index + 1}: {cells}")

            # Überprüfen, ob die Zeilenlänge mit der Anzahl der Header übereinstimmt
            if len(cells) != len(headers) + 1:
                raise RuntimeError(f"Line {row_index + 1} has incorrect length")

            row_header = cells[0]
            row_values = cells[1:]

            # Überprüfen, ob die Kopfzeilen der Spalten mit der Zeile übereinstimmen
            if row_header != headers[row_index]:
                raise RuntimeError(f"Row header mismatch at line {row_index + 1}")

            for col_index, value in enumerate(row_values):
                if value:  # Nur falls eine Kante existiert (kein leerer String)
                    weight = float(value)
                    self.add_edge_by_indices(row_index, col_index, weight)

    def read_graph_from_adjacency_matrix_file(self, filename: str) -> None:
        """
        Liest eine Adjazenzmatrix aus einer Datei und setzt den Graphen entsprechend.
        """
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Debugging: print the lines read from the file
        print(f"Lines read from file: {lines}")

        self.set_adjacency_matrix([line.strip() for line in lines])

    def __str__(self) -> str:
        # Printe in diesem Format
        # A -> [('B', 1.0), ('C', 3.0), ('D', 1.0)]
        # B -> [('A', 1.0), ('E', 3.0), ('F', 3.0)]
        # C -> [('A', 3.0), ('D', 1.0), ('G', 1.0)]
        # D -> [('A', 1.0), ('C', 1.0), ('E', 1.0), ('G', 2.0)]
        # E -> [('B', 3.0), ('D', 1.0), ('F', 1.0), ('H', 5.0)]
        # F -> [('B', 3.0), ('E', 1.0), ('H', 1.0)]
        # G -> [('C', 1.0), ('D', 2.0), ('H', 1.0)]
        # H -> [('E', 5.0), ('F', 1.0), ('G', 1.0)]
        return '\n'.join(f"{self._vertices[i]} -> {self.neighbors_for_index_with_weights(i)}" for i in range(self.vertex_count))




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
    graph.add_edge(Edge(0, 1, 1))

    print("Füge Kante von 'B' nach 'A' mit Index hinzu...")
    graph.add_edge_by_indices(1, 0, 2)

    print("Füge Kante von 'A' nach 'B' mit Knoten hinzu...")
    graph.add_edge_by_vertices('A', 'B', 3)

    print("-----------------------------------------------------")



    print(f"Aktuelle Anzahl Knoten: {graph.vertex_count}")
    print(f"Aktuelle Anzahl Kanten: {graph.edge_count}")

    print("-----------------------------------------------------")

    print("Wer hat den Index 0?")
    print(graph.vertex_at(0))

    print("Welchen Index hat 'B'?")
    print(graph.index_of('B'))

    print("Nachbarn von 'A' mit Gewichtung:")
    print(graph.neighbors_for_index_with_weights(0))

    print("Welche Kanten hat 'A'?")
    print(graph.edges_for_index(0))


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
    filename = "Graph_A-H.csv"
    g = Graph()
    g.read_graph_from_adjacency_matrix_file(filename)
    print(g)




# #Ein Graph G = (V, E, w) besteht aus
# #1. einer Menge V von Knoten (vertex)
# #2. einer Menge E von Kanten (edge) zwischen einigen der Knoten
# #3. (einer Gewichtsfunktion)