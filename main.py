import networkx as nx
import k_shortest
from ui import SimpleGraphUI
from typing import List, Any, Tuple
from cycles import find_all_cycles as _find_all_cycles_func

# Обгортка для find_all_cycles, яка створює неорієнтований граф (nx.Graph)
# з вхідного списку ребер.
def find_all_cycles(edges: List[Tuple[Any, Any, float]]) -> List[List[Any]]:
    G = nx.Graph() # Використовуємо nx.Graph для неорієнтованого графа
    for u, v, _ in edges:
        G.add_edge(u, v)

    G_dict = nx.to_dict_of_lists(G)

    # 3. Викликаємо функцію з модуля cycles.py, яка очікує dict
    return _find_all_cycles_func(G_dict)

# --- K найкоротших шляхів ---
def find_k_shortest(edges, start, end, K):
    # K-найкоротших шляхів зазвичай працює на орієнтованому графі
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)

    result = k_shortest.find_k_shortest_paths(G, start, end, K)

    print("\nРезультат Алгоритму Єна:")
    for i, (cost, path) in enumerate(result, start=1):
        print(f"  {i}-й шлях: {' -> '.join(path)}, довжина = {cost}")

    return result

if __name__ == "__main__":
    # Тепер ui використовує імпортовану обгортку для циклів
    ui = SimpleGraphUI(find_k_shortest, find_all_cycles)
    ui.run()