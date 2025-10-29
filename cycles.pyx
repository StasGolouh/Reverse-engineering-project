# cycles.py (або cycles.pyx)
# cython: language_level=3

from typing import List, Tuple, Dict, Any, Set

def find_all_cycles(G: Dict[Any, List[Any]]) -> List[List[Any]]:

    all_cycles = []
    # visited_global залишаємо для перебору компонентів,
    # але вузли не додаються в ній під час DFS.
    visited_global: Set[Any] = set()

    # Перебираємо всі вузли як початкові
    for start_node in G.keys():
        # Додаємо вузол до visited_global перед початком DFS
        if start_node not in visited_global:
            _dfs_find_cycles(G, start_node, None, [], all_cycles, visited_global)

    # === ВИПРАВЛЕНА НОРМАЛІЗАЦІЯ ===
    unique_cycles = []
    seen = set()
    for cycle in all_cycles:
        N = len(cycle)
        if N < 3:  # Цикли мають бути не менше 3 вузлів
            continue

        # 1. Збираємо всі 2N можливих представлень циклу
        # (N ротацій оригінального і N ротацій реверсу)
        double_cycle = cycle + cycle
        reversed_cycle_raw = list(reversed(cycle))
        reversed_double_cycle = reversed_cycle_raw + reversed_cycle_raw

        all_rotations = []
        for i in range(N):
            # Ротація оригінального (Напрямок A)
            all_rotations.append(double_cycle[i:i + N])
            # Ротація реверсу (Напрямок B)
            all_rotations.append(reversed_double_cycle[i:i + N])

        # 2. Визначаємо лексикографічно найменшу форму (Канонічну)
        # Порівнюємо як кортежі для надійної послідовності
        cycle_list_canonical = min(all_rotations, key=lambda x: tuple(x))
        cycle_tuple_canonical = tuple(cycle_list_canonical)

        # 3. Додаємо лише, якщо ще не бачили
        if cycle_tuple_canonical not in seen:
            seen.add(cycle_tuple_canonical)
            unique_cycles.append(list(cycle_list_canonical))

    return unique_cycles

def _dfs_find_cycles(G: Dict[Any, List[Any]],
                     current: Any,
                     parent: Any,
                     path: List[Any],
                     cycles_list: List[List[Any]],
                     visited_global: Set[Any]):
    path.append(current)

    for neighbor in G.get(current, []):
        if neighbor == parent:
            continue

        if neighbor in path:
            cycle_start_idx = path.index(neighbor)
            cycle = path[cycle_start_idx:]
            cycles_list.append(cycle)
            continue

        if neighbor not in visited_global:
            _dfs_find_cycles(G, neighbor, current, path, cycles_list, visited_global)

    path.pop()