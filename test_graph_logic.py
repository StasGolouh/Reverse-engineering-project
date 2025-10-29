import unittest
import sys
import io

# Імпортуємо функції з вашого файлу
try:
    from main import find_all_cycles, find_k_shortest
except ImportError:
    print("Помилка: Не вдалося імпортувати 'graph_logic'.")
    print("Переконайтеся, що ваш основний файл називається 'graph_logic.py' і знаходиться в тій самій директорії.")
    sys.exit(1)


class TestGraphLogic(unittest.TestCase):

    # --- Тести для find_all_cycles ---

    def test_cycles_empty_graph(self):
        """Перевіряє, що порожній граф не має циклів."""
        print(f"\n--- {self.id()} ---")
        edges = []
        expected = []
        print(f"Вхід (ребра): {edges}")
        print(f"Очікується: {expected}")

        result = find_all_cycles(edges)
        print(f"Результат: {result}")
        self.assertEqual(result, expected)

    def test_cycles_no_cycle(self):
        """Перевіряє граф без циклів (простий шлях/дерево)."""
        print(f"\n--- {self.id()} ---")
        edges = [('A', 'B', 1), ('B', 'C', 1), ('C', 'D', 1)]
        expected = []
        print(f"Вхід (ребра): {edges}")
        print(f"Очікується: {expected}")

        result = find_all_cycles(edges)
        print(f"Результат: {result}")
        self.assertEqual(result, expected)

    def test_cycles_simple_triangle(self):
        """Перевіряє один простий цикл (трикутник) та його нормалізацію."""
        print(f"\n--- {self.id()} ---")
        edges = [('A', 'B', 1), ('B', 'C', 1), ('C', 'A', 1)]
        expected = [['A', 'B', 'C']]
        print(f"Вхід (ребра): {edges}")
        print(f"Очікується: {expected}")

        result = find_all_cycles(edges)
        print(f"Результат: {result}")
        self.assertEqual(result, expected)

    def test_cycles_triangle_different_order(self):
        """Перевіряє, що порядок ребер не впливає на нормалізований результат."""
        print(f"\n--- {self.id()} ---")
        edges = [('C', 'A', 1), ('B', 'C', 1), ('A', 'B', 1)]
        expected = [['A', 'B', 'C']]
        print(f"Вхід (ребра): {edges}")
        print(f"Очікується: {expected}")

        result = find_all_cycles(edges)
        print(f"Результат: {result}")
        self.assertEqual(result, expected)

    def test_cycles_simple_square(self):
        """Перевіряє один цикл (квадрат) та його нормалізацію."""
        print(f"\n--- {self.id()} ---")
        edges = [('A', 'B', 1), ('B', 'C', 1), ('C', 'D', 1), ('D', 'A', 1)]
        expected = [['A', 'B', 'C', 'D']]
        print(f"Вхід (ребра): {edges}")
        print(f"Очікується: {expected}")

        result = find_all_cycles(edges)
        print(f"Результат: {result}")
        self.assertEqual(result, expected)

    def test_cycles_bowtie(self):
        """Перевіряє два цикли, що ділять одну вершину."""
        print(f"\n--- {self.id()} ---")
        edges = [
            ('A', 'B', 1), ('B', 'C', 1), ('C', 'A', 1),
            ('C', 'D', 1), ('D', 'E', 1), ('E', 'C', 1)
        ]
        expected = [['A', 'B', 'C'], ['C', 'D', 'E']]
        print(f"Вхід (ребра): {edges}")
        print(f"Очікується: {expected}")

        result = find_all_cycles(edges)
        print(f"Результат: {result}")
        self.assertCountEqual(result, expected)

    def test_cycles_complex_graph(self):
        """Перевіряє більш складний граф (квадрат з діагоналлю)."""
        print(f"\n--- {self.id()} ---")
        edges = [
            ('A', 'B', 1), ('B', 'C', 1), ('C', 'D', 1),
            ('D', 'A', 1), ('B', 'D', 1)
        ]
        expected = [['B', 'C', 'D'], ['A', 'B', 'C', 'D']]
        print(f"Вхід (ребра): {edges}")
        print(f"Очікується: {expected}")

        result = find_all_cycles(edges)
        print(f"Результат: {result}")
        self.assertCountEqual(result, expected)

    def test_cycles_disconnected_graph(self):
        """Перевіряє незв'язний граф з циклами у кожній компоненті."""
        print(f"\n--- {self.id()} ---")
        edges = [
            ('A', 'B', 1), ('B', 'C', 1), ('C', 'A', 1),
            ('X', 'Y', 1), ('Y', 'Z', 1), ('Z', 'X', 1)
        ]
        expected = [['A', 'B', 'C'], ['X', 'Y', 'Z']]
        print(f"Вхід (ребра): {edges}")
        print(f"Очікується: {expected}")

        result = find_all_cycles(edges)
        print(f"Результат: {result}")
        self.assertCountEqual(result, expected)

    # --- Тести для find_k_shortest ---

    # Ми ВИДАЛИЛИ методи setUp та tearDown,
    # оскільки вони більше не потрібні

    def test_k_shortest_simple_path(self):
        """Перевіряє знаходження K найкоротших шляхів у простому графі."""
        print(f"\n--- {self.id()} ---")
        edges = [
            ('A', 'B', 2), ('A', 'C', 10), ('B', 'D', 5),
            ('C', 'D', 1), ('B', 'C', 3)
        ]
        start, end, K = 'A', 'D', 3
        expected = [
            (6.0, ['A', 'B', 'C', 'D']),
            (7.0, ['A', 'B', 'D']),
            (11.0, ['A', 'C', 'D'])
        ]

        print(f"Вхід (ребра): {edges}")
        print(f"Вхід (start, end, K): ('{start}', '{end}', {K})")
        print(f"Очікується: {expected}")

        result = find_k_shortest(edges, start, end, K)
        print(f"Результат: {result}")
        self.assertEqual(result, expected)

    def test_k_shortest_no_path(self):
        """Перевіряє випадок, коли шлях між вузлами не існує."""
        print(f"\n--- {self.id()} ---")
        edges = [('A', 'B', 1), ('C', 'D', 1)]
        start, end, K = 'A', 'D', 2
        expected = []

        print(f"Вхід (ребра): {edges}")
        print(f"Вхід (start, end, K): ('{start}', '{end}', {K})")
        print(f"Очікується: {expected}")

        result = find_k_shortest(edges, start, end, K)
        print(f"Результат: {result}")
        self.assertEqual(result, expected)

    def test_k_shortest_k_more_than_paths(self):
        """Перевіряє, що K > (кількість шляхів) повертає всі наявні шляхи."""
        print(f"\n--- {self.id()} ---")
        edges = [
            ('A', 'B', 2), ('A', 'C', 10), ('B', 'D', 5),
            ('C', 'D', 1), ('B', 'C', 3)
        ]
        start, end, K = 'A', 'D', 5
        expected = [
            (6.0, ['A', 'B', 'C', 'D']),
            (7.0, ['A', 'B', 'D']),
            (11.0, ['A', 'C', 'D'])
        ]

        print(f"Вхід (ребра): {edges}")
        print(f"Вхід (start, end, K): ('{start}', '{end}', {K})")
        print(f"Очікується: {expected}")

        result = find_k_shortest(edges, start, end, K)
        print(f"Результат: {result}")
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_k_shortest_start_equals_end(self):
        """Перевіряє випадок, коли початковий та кінцевий вузол збігаються."""
        print(f"\n--- {self.id()} ---")
        edges = [('A', 'B', 2), ('B', 'A', 3)]
        start, end, K = 'A', 'A', 2
        expected = [(0, ['A'])]

        print(f"Вхід (ребра): {edges}")
        print(f"Вхід (start, end, K): ('{start}', '{end}', {K})")
        print(f"Очікується: {expected}")

        result = find_k_shortest(edges, start, end, K)
        print(f"Результат: {result}")
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()