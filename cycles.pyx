# cython: language_level=3
from sage.all import Graph

def find_all_cycles(graph):

    all_cycles = []

    # Ми будемо використовувати множину (set) для відвіданих вузлів,
    # щоб не починати пошук з одного вузла декілька разів.
    visited_nodes = set()

    # Нам потрібно пройти по кожному вузлу,
    # оскільки граф може бути незв'язним.
    for start_node in graph.vertices():
        if start_node not in visited_nodes:
            # Запускаємо рекурсивний помічник
            # `path` - це наш поточний шлях (стек)
            # `parent` - вузол, з якого ми прийшли
            _dfs_recursive_helper(graph, start_node, None, [], all_cycles, visited_nodes)

    # Потрібно відфільтрувати дублікати циклів
    # (наприклад, [1, 2, 3] і [1, 3, 2] - це той самий цикл)
    return all_cycles


def _dfs_recursive_helper(graph, current_node, parent_node, path, cycles_list, visited_set):

    # 1. Додаємо поточний вузол до шляху
    path.append(current_node)

    # 2. Перебираємо всіх сусідів
    for neighbor in graph.neighbors(current_node):

        # 3. Випадок 1: Ігноруємо батька (вузол, з якого прийшли)
        if neighbor == parent_node:
            continue

        # 4. Випадок 2: Знайдено цикл (сусід вже є у поточному шляху)
        if neighbor in path:
            # Ми знайшли "зворотне ребро"
            # Витягуємо цикл зі шляху
            cycle = path[path.index(neighbor):]
            cycles_list.append(cycle)
            # Ми не зупиняємося, а продовжуємо шукати інші цикли
            continue

        # 5. Випадок 3: Продовжуємо пошук (якщо вузол ще не відвідували)
        # (Перевірка на visited_set допомагає уникнути повторного обходу
        # вже повністю досліджених гілок)
        if neighbor not in visited_set:
            _dfs_recursive_helper(graph, neighbor, current_node, path, cycles_list, visited_set)

    # 6. Відкат (Backtracking):
    # Коли ми дослідили всіх сусідів, видаляємо вузол зі шляху
    # і позначаємо як повністю відвіданий.
    path.pop()
    visited_set.add(current_node)


# --- Приклад використання (для перевірки працездатності) ---
if __name__ == "__main__":
    # Це приклад того, як Студент 3 (Назар) буде тестувати ваш код [cite: 44]

    # Використовуємо SageMath для створення графа [cite: 19]
    # Граф "трикутник" [cite: 47]
    G_triangle = Graph({0: [1, 2], 1: [2]})

    print("Шукаємо цикли у 'трикутнику':")
    cycles_tri = find_all_cycles(G_triangle)
    print(cycles_tri)  # Має вивести щось типу [[0, 1, 2]]

    # Граф "квадрат" [cite: 47]
    G_square = Graph({0: [1, 3], 1: [2], 2: [3]})
    print("\nШукаємо цикли у 'квадраті':")
    cycles_sq = find_all_cycles(G_square)
    print(cycles_sq)  # Має вивести щось типу [[0, 1, 2, 3]]

    # Граф "метелик" (bowtie) [cite: 47]
    # Два трикутники, з'єднані в одній точці (2)
    G_bowtie = Graph({0: [1, 2], 1: [2], 2: [3, 4], 3: [4]})
    print("\nШукаємо цикли у 'метелику':")
    cycles_bow = find_all_cycles(G_bowtie)
    print(cycles_bow)  # Має вивести [[0, 1, 2], [2, 3, 4]]