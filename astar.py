import heapq
import json
import math


def manhattan_heuristic(node, goal):
    """
    Computes the Manhattan distance heuristic between two geographical points using lat/lon.

    Args:
        node: The current node as (lat, lon).
        goal: The goal node as (lat, lon).

    Returns:
        Manhattan distance approximation (ignoring Earth's curvature).
    """
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])


def weighted_astar(graph, start, goal, node_positions, weight_factor=1.0):
    """
    Weighted A* search algorithm with Manhattan heuristic.

    Args:
        graph: A dictionary where keys are nodes and values are lists of (neighbor, cost) tuples.
        start: The starting node.
        goal: The goal node.
        node_positions: A dictionary mapping nodes to their (lat, lon) positions.
        weight_factor: The weight to apply to the heuristic in the evaluation function.

    Returns:
        A tuple containing (path, cost) where:
        - path is the list of nodes from start to goal.
        - cost is the total cost of the path.
    """
    open_set = []
    heapq.heappush(open_set, (0, start))

    g_cost = {start: 0}
    came_from = {}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_cost[goal]

        for neighbor, cost in graph.get(current, []):
            tentative_g = g_cost[current] + cost
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                heuristic_cost = manhattan_heuristic(
                    node_positions[current], node_positions[goal]
                )
                f_cost = tentative_g + heuristic_cost
                heapq.heappush(open_set, (f_cost, neighbor))
                came_from[neighbor] = current

    return None, float("inf")  # No path found


# Parsing nodes and edges
def parse_graph(data):
    graph = {}
    node_positions = {}

    # Create node positions mapping
    for node in data["nodes"]:
        node_positions[node["id"]] = (node["lat"], node["lon"])

    # Create adjacency list
    for edge in data["edges"]:
        source = edge["source"]
        target = edge["target"]
        weight = edge["weight"]

        if source not in graph:
            graph[source] = []
        if target not in graph:
            graph[target] = []

        graph[source].append((target, weight))
        graph[target].append((source, weight))  # Assuming the graph is undirected

    return graph, node_positions


# Example usage
if __name__ == "__main__":
    # Sample data
    with open("graph.json", "r") as f:
        data = json.load(f)

    graph = data["edges"]
    node_positions = data["nodes"]
    graph, node_positions = parse_graph(data)
    start = "G08"
    goal = "A36"
    weight_factor = 1.5

    # Run Weighted A*
    path, cost = weighted_astar(graph, start, goal, node_positions, weight_factor)
    print("Path:", path)
    print("Cost:", cost)
