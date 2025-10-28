import networkx as nx
from ui import SimpleGraphUI
from typing import List, Any, Tuple

def find_all_cycles(edges: List[Tuple[Any, Any, float]]) -> List[List[Any]]:
    G = nx.Graph()
    for u, v, _ in edges:
        G.add_edge(u, v)

    all_cycles = []
    visited = set()
    for start_node in G.nodes():
        if start_node not in visited:
            _dfs_find_cycles(G, start_node, None, [], all_cycles, visited)

    # Видаляємо дублікати
    unique_cycles = []
    seen = set()
    for cycle in all_cycles:
        min_idx = cycle.index(min(cycle))
        rotated = cycle[min_idx:] + cycle[:min_idx]
        rev_rotated = list(reversed(rotated))
        min_rotated = min(rotated, rev_rotated, key=lambda x: tuple(x))
        cycle_tuple = tuple(min_rotated)
        if cycle_tuple not in seen:
            seen.add(cycle_tuple)
            unique_cycles.append(list(min_rotated))

    return unique_cycles

def _dfs_find_cycles(G, current, parent, path, cycles_list, visited):
    path.append(current)
    for neighbor in G.neighbors(current):
        if neighbor == parent:
            continue
        if neighbor in path:
            cycle_start_idx = path.index(neighbor)
            cycle = path[cycle_start_idx:]
            cycles_list.append(cycle)
            continue
        if neighbor not in visited:
            _dfs_find_cycles(G, neighbor, current, path, cycles_list, visited)
    path.pop()
    visited.add(current)

# --- K найкоротших шляхів ---
def find_k_shortest_paths(edges: List[Tuple[Any, Any, float]], start, end, K):
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    # Приклад: тут можна викликати власний k_shortest алгоритм
    try:
        length, path = nx.single_source_dijkstra(G, start, end)
        return [(length, path)]
    except nx.NetworkXNoPath:
        return []

if __name__ == "__main__":
    ui = SimpleGraphUI(find_k_shortest_paths, find_all_cycles)
    ui.run()