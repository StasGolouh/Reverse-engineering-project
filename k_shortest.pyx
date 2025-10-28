from heapq import heappush, heappop

def dijkstra_nx(graph, source, target):
    """Пошук найкоротшого шляху (Дейкстра)"""
    queue = [(0, source, [])]
    seen = set()

    while queue:
        cost, node, path = heappop(queue)
        if node in seen:
            continue

        path = path + [node]
        seen.add(node)

        if node == target:
            return cost, path

        if node not in graph:
            continue

        for neighbor, attributes in graph[node].items():
            if neighbor not in seen:
                weight = attributes.get('weight', 1)
                heappush(queue, (cost + weight, neighbor, path))

    return float("inf"), []


def get_path_cost(graph, path):
    """Підрахунок вартості шляху."""
    total_cost = 0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if graph.has_edge(u, v):
            total_cost += graph[u][v].get('weight', 1)
        else:
            return float('inf')
    return total_cost


def find_k_shortest_paths(graph, source, target, int K):
    """Алгоритм Єна"""
    final_paths = []
    candidate_paths = []

    cost, path = dijkstra_nx(graph, source, target)
    if not path:
        return []

    final_paths.append((cost, path))

    for k in range(1, K):
        if not final_paths:
            break

        last_cost, last_path = final_paths[-1]

        for i in range(len(last_path) - 1):
            spur_node = last_path[i]
            root_path = last_path[:i + 1]
            temp_graph = graph.copy()

            for cost_p, path_p in final_paths:
                if len(path_p) > i and path_p[:i + 1] == root_path:
                    u = path_p[i]
                    v = path_p[i + 1]
                    if temp_graph.has_edge(u, v):
                        temp_graph.remove_edge(u, v)

            for node in root_path:
                if node != spur_node:
                    if node in temp_graph:
                        temp_graph.remove_node(node)

            spur_cost, spur_path = dijkstra_nx(temp_graph, spur_node, target)

            if spur_path:
                total_path = root_path[:-1] + spur_path
                total_cost = get_path_cost(graph, total_path)
                candidate = (total_cost, total_path)

                if candidate not in candidate_paths and candidate not in final_paths:
                    candidate_paths.append(candidate)

        if not candidate_paths:
            break

        candidate_paths.sort()
        best_candidate = candidate_paths.pop(0)
        final_paths.append(best_candidate)

    return final_paths