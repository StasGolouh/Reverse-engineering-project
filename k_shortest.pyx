from heapq import heappush, heappop

def dijkstra_nx(graph, source, target):
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
    """Підрахунок вартості шляху в оригінальному графі."""
    total_cost = 0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        if graph.has_edge(u, v):
            total_cost += graph[u][v].get('weight', 1)
        else:
            return float('inf')
    return total_cost

def find_k_shortest_paths(graph, source, target, K: int):
    final_paths = []
    candidate_paths_heap = []
    final_paths_set = set()

    # 1. Знаходимо 1-й найкоротший шлях
    cost, path = dijkstra_nx(graph, source, target)
    if not path:
        return []  # Немає шляхів

    final_paths.append((cost, path))
    final_paths_set.add(tuple(path))

    # 2. Починаємо цикл для пошуку шляхів з 2-го по K-й
    for k in range(1, K):

        if not final_paths:
            break

        last_cost, last_path = final_paths[-1]

        # 3. Ітеруємо по вузлах останнього шляху
        for i in range(len(last_path) - 1):
            spur_node = last_path[i]
            root_path = last_path[:i + 1]

            temp_graph = graph.copy()

            # A) Видаляємо ребра, які є частиною *вже знайдених* шляхів
            for cost_p, path_p in final_paths:
                if len(path_p) > i and path_p[:i + 1] == root_path:
                    u = path_p[i]
                    v = path_p[i + 1]
                    if temp_graph.has_edge(u, v):
                        temp_graph.remove_edge(u, v)

            # B) Видаляємо вузли з root_path (окрім spur_node)
            for node in root_path:
                if node != spur_node:
                    if node in temp_graph:
                        temp_graph.remove_node(node)

            # 4. Знаходимо "шлях-відхилення" (spur_path)
            spur_cost, spur_path = dijkstra_nx(temp_graph, spur_node, target)

            # 5. Якщо відхилення знайдено, збираємо повний шлях
            if spur_path:
                total_path = root_path[:-1] + spur_path
                # Перераховуємо вартість на ОРИГІНАЛЬНОМУ графі
                total_cost = get_path_cost(graph, total_path)
                candidate = (total_cost, total_path)

                if tuple(total_path) not in final_paths_set:
                    heappush(candidate_paths_heap, candidate)

        # 6. Обираємо найкращого кандидата з черги
        if not candidate_paths_heap:
            break  # Немає більше кандидатів

        # Витягуємо, доки не знайдемо *новий* шлях
        best_cost, best_path = heappop(candidate_paths_heap)
        while tuple(best_path) in final_paths_set:
            if not candidate_paths_heap:
                break
            best_cost, best_path = heappop(candidate_paths_heap)

        if tuple(best_path) in final_paths_set:
            break

        # 7. Ми знайшли K-й найкоротший шлях
        final_paths.append((best_cost, best_path))
        final_paths_set.add(tuple(best_path))

    return final_paths