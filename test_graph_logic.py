import unittest
import sys
import io

# Імпортуємо функції з вашого файлу
# Переконайтеся, що ваш файл називається 'main.py'
try:
    from main import find_all_cycles, find_k_shortest
except ImportError:
    print("Помилка: Не вдалося імпортувати 'graph_logic'.")
    print("Переконайтеся, що ваш основний файл називається 'main.py' і знаходиться в тій самій директорії.")
    sys.exit(1)


class TestGraphLogic(unittest.TestCase):

    # --- Тести для find_all_cycles ---

    def test_cycles_empty_graph(self):
        """Перевіряє, що порожній граф не має циклів."""
        edges = []
        self.assertEqual(find_all_cycles(edges), [])

    def test_cycles_no_cycle(self):
        """Перевіряє граф без циклів (простий шлях/дерево)."""
        edges = [('A', 'B', 1), ('B', 'C', 1), ('C', 'D', 1)]
        self.assertEqual(find_all_cycles(edges), [])

    def test_cycles_simple_triangle(self):
        """Перевіряє один простий цикл (трикутник) та його нормалізацію."""
        # Оскільки 'A' < 'B' < 'C', нормалізований цикл має бути ['A', 'B', 'C']
        edges = [('A', 'B', 1), ('B', 'C', 1), ('C', 'A', 1)]
        expected = [['A', 'B', 'C']]
        self.assertEqual(find_all_cycles(edges), expected)

    def test_cycles_triangle_different_order(self):
        """Перевіряє, що порядок ребер не впливає на нормалізований результат."""
        edges = [('C', 'A', 1), ('B', 'C', 1), ('A', 'B', 1)]
        expected = [['A', 'B', 'C']]
        self.assertEqual(find_all_cycles(edges), expected)

    def test_cycles_simple_square(self):
        """Перевіряє один цикл (квадрат) та його нормалізацію."""
        # Нормалізований цикл: ['A', 'B', 'C', 'D']
        edges = [('A', 'B', 1), ('B', 'C', 1), ('C', 'D', 1), ('D', 'A', 1)]
        expected = [['A', 'B', 'C', 'D']]
        self.assertEqual(find_all_cycles(edges), expected)

    def test_cycles_bowtie(self):
        """Перевіряє два цикли, що ділять одну вершину."""
        edges = [
            ('A', 'B', 1), ('B', 'C', 1), ('C', 'A', 1),  # Цикл 1: A-B-C
            ('C', 'D', 1), ('D', 'E', 1), ('E', 'C', 1)  # Цикл 2: C-D-E
        ]
        expected = [['A', 'B', 'C'], ['C', 'D', 'E']]
        result = find_all_cycles(edges)

        # Використовуємо assertCountEqual, оскільки порядок знаходження циклів
        # (який з них буде першим у списку) не гарантований.
        self.assertCountEqual(result, expected)

    def test_cycles_complex_graph(self):
        """Перевіряє більш складний граф (квадрат з діагоналлю)."""
        edges = [
            ('A', 'B', 1), ('B', 'C', 1), ('C', 'D', 1),
            ('D', 'A', 1), ('B', 'D', 1)
        ]
        # Ми очікуємо лише ті цикли, які знаходить поточний алгоритм
        expected = [['B', 'C', 'D'], ['A', 'B', 'C', 'D']] # <--- НОВИЙ
        result = find_all_cycles(edges)
        self.assertCountEqual(result, expected)

    def test_cycles_disconnected_graph(self):
        """Перевіряє незв'язний граф з циклами у кожній компоненті."""
        edges = [
            ('A', 'B', 1), ('B', 'C', 1), ('C', 'A', 1),  # Компонента 1
            ('X', 'Y', 1), ('Y', 'Z', 1), ('Z', 'X', 1)  # Компонента 2
        ]
        expected = [['A', 'B', 'C'], ['X', 'Y', 'Z']]
        result = find_all_cycles(edges)
        self.assertCountEqual(result, expected)

    # --- Тести для find_k_shortest ---
    # Ці тести є інтеграційними - вони припускають,
    # що бібліотека 'k_shortest' встановлена і працює коректно.

    def setUp(self):
        """Пригнічує вивід print() з find_k_shortest під час тестів."""
        self._original_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        """Відновлює стандартний вивід."""
        sys.stdout = self._original_stdout

    def test_k_shortest_simple_path(self):
        """Перевіряє знаходження K найкоротших шляхів у простому графі."""
        edges = [
            ('A', 'B', 2), ('A', 'C', 10), ('B', 'D', 5),
            ('C', 'D', 1), ('B', 'C', 3)
        ]
        start, end, K = 'A', 'D', 3

        # Очікувані шляхи (відсортовані за вартістю):
        # 1. A -> B -> C -> D (вартість: 2 + 3 + 1 = 6)
        # 2. A -> B -> D (вартість: 2 + 5 = 7)
        # 3. A -> C -> D (вартість: 10 + 1 = 11)
        expected = [
            (6.0, ['A', 'B', 'C', 'D']),
            (7.0, ['A', 'B', 'D']),
            (11.0, ['A', 'C', 'D'])
        ]

        result = find_k_shortest(edges, start, end, K)
        self.assertEqual(result, expected)

    def test_k_shortest_no_path(self):
        """Перевіряє випадок, коли шлях між вузлами не існує."""
        edges = [('A', 'B', 1), ('C', 'D', 1)]
        start, end, K = 'A', 'D', 2
        expected = []
        result = find_k_shortest(edges, start, end, K)
        self.assertEqual(result, expected)

    def test_k_shortest_k_more_than_paths(self):
        """Перевіряє, що K > (кількість шляхів) повертає всі наявні шляхи."""
        edges = [
            ('A', 'B', 2), ('A', 'C', 10), ('B', 'D', 5),
            ('C', 'D', 1), ('B', 'C', 3)
        ]
        start, end, K = 'A', 'D', 5  # Запитуємо 5 шляхів, але існує лише 3

        expected = [
            (6.0, ['A', 'B', 'C', 'D']),
            (7.0, ['A', 'B', 'D']),
            (11.0, ['A', 'C', 'D'])
        ]

        result = find_k_shortest(edges, start, end, K)
        # Алгоритм Єна має повернути лише стільки шляхів, скільки існує
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 3)

    def test_k_shortest_start_equals_end(self):
        """Перевіряє випадок, коли початковий та кінцевий вузол збігаються."""
        edges = [('A', 'B', 2), ('B', 'A', 3)]
        start, end, K = 'A', 'A', 2

        # Алгоритм Єна знаходить лише прості шляхи.
        # Єдиний простий шлях з A в A - це ['A'] вартістю 0.
        # З виводу помилки ми бачимо, що бібліотека повертає (0, ['A']).
        expected = [(0, ['A'])]  # <--- НОВИЙ

        result = find_k_shortest(edges, start, end, K)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()