import unittest
import math
from optimizador_rutas.algoritmo.algoritmo_calculo_ruta import haversine, create_graph, dijkstra, calcular_mejor_ruta

class TestHaversine(unittest.TestCase):

    def test_haversine(self):
        # Test coordinates
        coord1 = (0, 0)  # Equator and Prime Meridian
        coord2 = (0, 90)  # Equator and 90 degrees East

        # Expected distance (quarter of Earth's circumference)
        R = 6371  # Earth radius in kilometers
        expected_distance = (math.pi / 2) * R

        # Call the function
        result = haversine(coord1, coord2)

        # Assertions
        self.assertAlmostEqual(result, expected_distance, places=2)

    def test_haversine_zero_distance(self):
        # Test with the same coordinates
        coord = (10, 20)
        result = haversine(coord, coord)
        self.assertEqual(result, 0)

    def test_haversine_known_distance(self):
        # Test with known distance between two points
        coord1 = (36.12, -86.67)  # Nashville, TN
        coord2 = (33.94, -118.40)  # Los Angeles, CA

        # Expected distance (approximate)
        expected_distance = 2886  # in kilometers

        # Call the function
        result = round(haversine(coord1, coord2))

        # Assertions
        self.assertAlmostEqual(result, expected_distance, places=2)

class TestDijkstra(unittest.TestCase):

    def test_dijkstra_simple_graph(self):
        # Simple graph with three nodes
        graph = {
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2},
            'C': {'A': 4, 'B': 2}
        }
        start = 'A'

        # Call the function
        distances, shortest_path = dijkstra(graph, start)

        # Expected results
        expected_distances = {'A': 0, 'B': 1, 'C': 3}
        expected_shortest_path = {'B': 'A', 'C': 'B'}

        # Assertions
        self.assertEqual(distances, expected_distances)
        self.assertEqual(shortest_path, expected_shortest_path)

    def test_dijkstra_disconnected_graph(self):
        # Graph with disconnected nodes
        graph = {
            'A': {'B': 1},
            'B': {'A': 1},
            'C': {}
        }
        start = 'A'

        # Call the function
        distances, shortest_path = dijkstra(graph, start)

        # Expected results
        expected_distances = {'A': 0, 'B': 1, 'C': float('inf')}
        expected_shortest_path = {'B': 'A'}

        # Assertions
        self.assertEqual(distances, expected_distances)
        self.assertEqual(shortest_path, expected_shortest_path)

    def test_dijkstra_complex_graph(self):
        # More complex graph
        graph = {
            'A': {'B': 1, 'C': 4, 'D': 7},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'A': 7, 'B': 5, 'C': 1}
        }
        start = 'A'

        # Call the function
        distances, shortest_path = dijkstra(graph, start)

        # Expected results
        expected_distances = {'A': 0, 'B': 1, 'C': 3, 'D': 4}
        expected_shortest_path = {'B': 'A', 'C': 'B', 'D': 'C'}

        # Assertions
        self.assertEqual(distances, expected_distances)
        self.assertEqual(shortest_path, expected_shortest_path)

    def test_dijkstra_single_node(self):
        # Graph with a single node
        graph = {
            'A': {}
        }
        start = 'A'

        # Call the function
        distances, shortest_path = dijkstra(graph, start)

        # Expected results
        expected_distances = {'A': 0}
        expected_shortest_path = {}

        # Assertions
        self.assertEqual(distances, expected_distances)
        self.assertEqual(shortest_path, expected_shortest_path)


class TestCreateGraph(unittest.TestCase):

    def test_create_graph_simple(self):
        punto_inicio = (0, 0)
        destinos = [(0, 90), (90, 0)]
        graph = create_graph(punto_inicio, destinos)

        # Expected graph structure
        expected_graph = {
            (0, 0): {(0, 90): haversine((0, 0), (0, 90)), (90, 0): haversine((0, 0), (90, 0))},
            (0, 90): {(0, 0): haversine((0, 90), (0, 0)), (90, 0): haversine((0, 90), (90, 0))},
            (90, 0): {(0, 0): haversine((90, 0), (0, 0)), (0, 90): haversine((90, 0), (0, 90))}
        }

        self.assertEqual(graph.keys(), expected_graph.keys())
        for key in graph:
            self.assertEqual(graph[key].keys(), expected_graph[key].keys())
            for sub_key in graph[key]:
                self.assertAlmostEqual(graph[key][sub_key], expected_graph[key][sub_key], places=2)

    def test_create_graph_single_destination(self):
        punto_inicio = (10, 10)
        destinos = [(20, 20)]
        graph = create_graph(punto_inicio, destinos)

        # Expected graph structure
        expected_graph = {
            (10, 10): {(20, 20): haversine((10, 10), (20, 20))},
            (20, 20): {(10, 10): haversine((20, 20), (10, 10))}
        }

        self.assertEqual(graph.keys(), expected_graph.keys())
        for key in graph:
            self.assertEqual(graph[key].keys(), expected_graph[key].keys())
            for sub_key in graph[key]:
                self.assertAlmostEqual(graph[key][sub_key], expected_graph[key][sub_key], places=2)

    def test_create_graph_no_destinations(self):
        punto_inicio = (0, 0)
        destinos = []
        graph = create_graph(punto_inicio, destinos)

        # Expected graph structure
        expected_graph = {
            (0, 0): {}
        }

        self.assertEqual(graph, expected_graph)

    def test_create_graph_multiple_destinations(self):
        punto_inicio = (0, 0)
        destinos = [(0, 90), (90, 0), (45, 45)]
        graph = create_graph(punto_inicio, destinos)

        # Check if all points are in the graph
        all_points = [punto_inicio] + destinos
        self.assertEqual(set(graph.keys()), set(map(tuple, all_points)))

        # Check if distances are symmetric
        for point1 in all_points:
            for point2 in all_points:
                if point1 != point2:
                    self.assertAlmostEqual(
                        graph[tuple(point1)][tuple(point2)],
                        graph[tuple(point2)][tuple(point1)],
                        places=2
                    )

class TestCalcularMejorRuta(unittest.TestCase):

    def test_calcular_mejor_ruta_simple(self):
        punto_inicio = (0, 0)
        destinos = [(0, 90), (90, 0)]
        result = calcular_mejor_ruta(punto_inicio, destinos)

        # Expected route (shortest path visiting all destinations)
        expected_route = [(0, 0), (0, 90), (90, 0)]
        self.assertEqual(result, expected_route)

    def test_calcular_mejor_ruta_single_destination(self):
        punto_inicio = (10, 10)
        destinos = [(20, 20)]
        result = calcular_mejor_ruta(punto_inicio, destinos)

        # Expected route
        expected_route = [(10, 10), (20, 20)]
        self.assertEqual(result, expected_route)

    def test_calcular_mejor_ruta_no_destinations(self):
        punto_inicio = (0, 0)
        destinos = []
        result = calcular_mejor_ruta(punto_inicio, destinos)

        # Expected route (only the starting point)
        expected_route = [(0, 0)]
        self.assertEqual(result, expected_route)

    def test_calcular_mejor_ruta_multiple_destinations(self):
        punto_inicio = (0, 0)
        destinos = [(0, 90), (90, 0), (45, 45)]
        ruta = calcular_mejor_ruta(punto_inicio, destinos)

        # Check if the route starts at the starting point
        self.assertEqual(ruta[0], punto_inicio)
        self.assertEqual(len(ruta), 4)

    def test_calcular_mejor_ruta_complex(self):
        punto_inicio = (0, 0)
        destinos = [(10, 10), (20, 20), (30, 30)]
        ruta = calcular_mejor_ruta(punto_inicio, destinos)

        self.assertEqual(ruta[0], punto_inicio)
        self.assertEqual(len(ruta), 4)


if __name__ == '__main__':
    unittest.main()