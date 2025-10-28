import networkx as nx
import k_shortest
from ui import SimpleGraphUI

def run_algorithm(edges, start, end, K):
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)

    result = k_shortest.find_k_shortest_paths(G, start, end, K)

    print("\nРезультат з вашого файлу (k_shortest.pyx):")
    for i, (cost, path) in enumerate(result, start=1):
        print(f"  {i}-й шлях: {' -> '.join(path)}, довжина = {cost}")

    return result

if __name__ == "__main__":
    ui = SimpleGraphUI(run_algorithm)
    ui.run()