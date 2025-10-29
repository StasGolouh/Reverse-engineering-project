# cycles.pyx
# cython: language_level=3

from typing import List, Tuple, Dict, Any

def find_all_cycles(G) -> List[List[Any]]:

    all_cycles = []
    visited = set()

    # Перебираємо всі вузли як початкові
    for start_node in G.nodes():
        if start_node not in visited:
            _dfs_find_cycles(G, start_node, None, [], all_cycles, visited)

    # Видаляємо дублікати циклів (цикли, що починаються з різних точок)
    unique_cycles = []
    seen = set()
    for cycle in all_cycles:
        # Нормалізуємо цикл: починаємо з мінімального вузла, обертаємо
        min_idx = cycle.index(min(cycle))
        rotated = cycle[min_idx:] + cycle[:min_idx]
        # Для неорієнтованого графа: враховуємо обидва напрямки
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
            continue  # ігноруємо зворотне ребро

        if neighbor in path:
            # Знайдено цикл
            cycle_start_idx = path.index(neighbor)
            cycle = path[cycle_start_idx:]
            cycles_list.append(cycle)
            continue

        if neighbor not in visited:
            _dfs_find_cycles(G, neighbor, current, path, cycles_list, visited)

    path.pop()
    visited.add(current)

# # --- Тестування (без Sage) ---
# if __name__ == "__main__":
#     import networkx as nx
#
#     print("Тестуємо пошук циклів (без SageMath)\n" + "=" * 50)
#
#     # Трикутник
#     G1 = nx.Graph()
#     G1.add_edges_from([(0, 1), (1, 2), (2, 0)])
#     print("Трикутник:", find_all_cycles(G1))
#
#     # Квадрат
#     G2 = nx.Graph()
#     G2.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
#     print("Квадрат:", find_all_cycles(G2))
#
#     # Метелик (два трикутники)
#     G3 = nx.Graph()
#     G3.add_edges_from([(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)])
#     print("Метелик:", find_all_cycles(G3))