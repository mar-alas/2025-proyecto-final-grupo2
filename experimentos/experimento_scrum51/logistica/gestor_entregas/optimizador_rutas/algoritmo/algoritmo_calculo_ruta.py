import heapq
import math

def haversine(coord1, coord2):
    # Calculate the great-circle distance between two points on the Earth
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def dijkstra(graph, start):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    shortest_path = {}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                shortest_path[neighbor] = current_node

    return distances, shortest_path

def create_graph(punto_inicio, destinos):
    graph = {}
    all_points = [punto_inicio] + destinos

    for i, point1 in enumerate(all_points):
        graph[tuple(point1)] = {}
        for j, point2 in enumerate(all_points):
            if i != j:
                graph[tuple(point1)][tuple(point2)] = haversine(point1, point2)

    return graph

def calcular_mejor_ruta(punto_inicio, destinos):
    graph = create_graph(punto_inicio, destinos)
    all_points = [punto_inicio] + destinos
    best_route = [punto_inicio]
    current_point = punto_inicio

    while destinos:
        distances, _ = dijkstra(graph, tuple(current_point))
        next_point = min(destinos, key=lambda x: distances[tuple(x)])
        best_route.append(next_point)
        current_point = next_point
        destinos.remove(next_point)

    return best_route

# pruebas
punto_inicio = (38.753495362702125, -121.38034016560347) # casa
destinos = [(38.77343079742246, -121.2708981742006), (38.83537069736703, -121.28506446296205), (38.78061339201902, -121.26790585696718)] # galeria, nuggets, costco
print(calcular_mejor_ruta(punto_inicio, destinos))