import tkinter as tk
from tkinter import messagebox

class SimpleGraphUI:
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Tk()
        self.root.title("K Shortest Paths")
        self.root.geometry("400x450")

        tk.Label(self.root, text="Пошук K найкоротших шляхів", font=("Arial", 12, "bold")).pack(pady=5)

        # --- Додавання ребер ---
        tk.Label(self.root, text="Додати ребро (з - до - вага):").pack()
        frame_add = tk.Frame(self.root)
        frame_add.pack(pady=2)

        self.from_entry = tk.Entry(frame_add, width=5)
        self.from_entry.grid(row=0, column=0)
        self.to_entry = tk.Entry(frame_add, width=5)
        self.to_entry.grid(row=0, column=1)
        self.weight_entry = tk.Entry(frame_add, width=5)
        self.weight_entry.grid(row=0, column=2)

        tk.Button(frame_add, text="Додати", command=self.add_edge).grid(row=0, column=3, padx=5)

        # --- Список ребер ---
        tk.Label(self.root, text="Ребра графа:").pack()
        self.edges_listbox = tk.Listbox(self.root, height=7, width=40)
        self.edges_listbox.pack()
        tk.Button(self.root, text="Видалити вибране", command=self.remove_edge).pack(pady=2)

        # --- Параметри ---
        tk.Label(self.root, text="Параметри:").pack()
        frame_params = tk.Frame(self.root)
        frame_params.pack(pady=2)

        tk.Label(frame_params, text="Початок:").grid(row=0, column=0)
        self.start_entry = tk.Entry(frame_params, width=5)
        self.start_entry.insert(0, "0")
        self.start_entry.grid(row=0, column=1)

        tk.Label(frame_params, text="Кінець:").grid(row=0, column=2)
        self.end_entry = tk.Entry(frame_params, width=5)
        self.end_entry.insert(0, "4")
        self.end_entry.grid(row=0, column=3)

        tk.Label(frame_params, text="K:").grid(row=0, column=4)
        self.k_entry = tk.Entry(frame_params, width=5)
        self.k_entry.insert(0, "3")
        self.k_entry.grid(row=0, column=5)

        # --- Кнопка пошуку ---
        tk.Button(self.root, text="Знайти шляхи", command=self.on_submit).pack(pady=5)

        # --- Результат ---
        tk.Label(self.root, text="Результат:").pack()
        self.output = tk.Text(self.root, height=8, width=45)
        self.output.pack()

        self.edges = []

    def add_edge(self):
        u = self.from_entry.get().strip()
        v = self.to_entry.get().strip()
        w = self.weight_entry.get().strip()

        if not u or not v or not w:
            messagebox.showwarning("Увага", "Заповніть усі поля!")
            return

        try:
            w = float(w)
        except ValueError:
            messagebox.showerror("Помилка", "Вага має бути числом.")
            return

        self.edges.append((u, v, w))
        self.edges_listbox.insert(tk.END, f"{u} -> {v} (вага={w})")

        self.from_entry.delete(0, tk.END)
        self.to_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)

    def remove_edge(self):
        sel = self.edges_listbox.curselection()
        if sel:
            index = sel[0]
            self.edges.pop(index)
            self.edges_listbox.delete(index)

    def on_submit(self):
        if not self.edges:
            messagebox.showwarning("Увага", "Немає жодного ребра!")
            return

        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        try:
            K = int(self.k_entry.get().strip())
            if K <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Помилка", "K має бути додатним числом.")
            return

        # Перевірка існування вершин
        vertices = {u for u, v, _ in self.edges} | {v for u, v, _ in self.edges}
        if start not in vertices:
            messagebox.showerror("Помилка", f"Вершина '{start}' не існує.")
            return
        if end not in vertices:
            messagebox.showerror("Помилка", f"Вершина '{end}' не існує.")
            return

        try:
            result = self.callback(self.edges, start, end, K)
            self.output.delete("1.0", tk.END)
            if not result:
                self.output.insert(tk.END, "Шляхи не знайдено.\n")
            else:
                for i, (cost, path) in enumerate(result, start=1):
                    self.output.insert(tk.END, f"{i}-й шлях: {' -> '.join(path)}, довжина = {cost}\n")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def run(self):
        self.root.mainloop()
