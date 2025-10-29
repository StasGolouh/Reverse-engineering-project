import tkinter as tk
from tkinter import messagebox, ttk


class SimpleGraphUI:
    def __init__(self, callback_paths, callback_cycles):
        self.callback_paths = callback_paths
        self.callback_cycles = callback_cycles

        self.root = tk.Tk()
        self.root.title("Графи: K шляхи та цикли")
        self.root.geometry("550x700")
        self.root.minsize(450, 600)

        # --- Налаштування стилю ---
        style = ttk.Style(self.root)
        try:
            style.theme_use('vista')
        except tk.TclError:
            print("Тема 'vista' не знайдена, використовується стандартна тема.")
            style.theme_use('default')

        style.configure('.', font=('Segoe UI', 10), padding=5)
        style.configure('TLabel', font=('Segoe UI', 11))
        style.configure('Header.TLabel', font=('Segoe UI', 13, 'bold'))
        style.configure('TButton', padding=(10, 5))
        style.configure('Danger.TButton', foreground='red', font=('Segoe UI', 10, 'bold'))

        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- 1. Додавання ребер ---
        lf_add = ttk.LabelFrame(main_frame, text=" 1. Додавання ребер ", padding=10)
        lf_add.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(lf_add, text="З:").grid(row=0, column=0, sticky='w')
        self.from_entry = ttk.Entry(lf_add, width=8)
        self.from_entry.grid(row=1, column=0, padx=(0, 10), sticky='w')

        ttk.Label(lf_add, text="До:").grid(row=0, column=1, sticky='w')
        self.to_entry = ttk.Entry(lf_add, width=8)
        self.to_entry.grid(row=1, column=1, padx=(0, 10), sticky='w')

        ttk.Label(lf_add, text="Вага:").grid(row=0, column=2, sticky='w')
        self.weight_entry = ttk.Entry(lf_add, width=8)
        self.weight_entry.grid(row=1, column=2, padx=(0, 10), sticky='w')

        lf_add.grid_columnconfigure(3, weight=1)
        self.add_button = ttk.Button(lf_add, text="Додати ребро", command=self.add_edge)
        self.add_button.grid(row=1, column=4, sticky='e')

        # --- 2. Список ребер ---
        lf_list = ttk.LabelFrame(main_frame, text=" 2. Список ребер ", padding=10)
        lf_list.pack(fill=tk.BOTH, expand=True, pady=10)

        list_frame = ttk.Frame(lf_list)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.edges_listbox = tk.Listbox(list_frame,
                                        height=7,
                                        yscrollcommand=scrollbar.set,
                                        font=('Consolas', 10),
                                        selectbackground="#0078d4",
                                        selectforeground="white")
        scrollbar.config(command=self.edges_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.edges_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.remove_button = ttk.Button(lf_list,
                                        text="Видалити вибране",
                                        command=self.remove_edge,
                                        style='Danger.TButton')
        self.remove_button.pack(pady=(10, 0), anchor='e')

        # --- 3. Параметри пошуку ---
        lf_params = ttk.LabelFrame(main_frame, text=" 3. Параметри пошуку ", padding=10)
        lf_params.pack(fill=tk.X, pady=10)
        lf_params.grid_columnconfigure((0, 1, 2), weight=1)

        ttk.Label(lf_params, text="Початок:").grid(row=0, column=0, sticky='w')
        self.start_entry = ttk.Entry(lf_params, width=8)
        self.start_entry.insert(0, "0")
        self.start_entry.grid(row=1, column=0, sticky='w')

        ttk.Label(lf_params, text="Кінець:").grid(row=0, column=1, sticky='w')
        self.end_entry = ttk.Entry(lf_params, width=8)
        self.end_entry.insert(0, "4")
        self.end_entry.grid(row=1, column=1, sticky='w')

        ttk.Label(lf_params, text="K (шляхів):").grid(row=0, column=2, sticky='w')
        self.k_entry = ttk.Entry(lf_params, width=8)
        self.k_entry.insert(0, "3")
        self.k_entry.grid(row=1, column=2, sticky='w')

        # --- Кнопки ---
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        buttons_frame.grid_columnconfigure((0, 1), weight=1)

        self.k_button = ttk.Button(buttons_frame, text="Знайти K-шляхи", command=self.on_submit)
        self.k_button.grid(row=0, column=0, sticky='ew', padx=(0, 5))

        self.cycles_button = ttk.Button(buttons_frame, text="Знайти всі цикли", command=self.on_find_cycles)
        self.cycles_button.grid(row=0, column=1, sticky='ew', padx=(5, 0))

        # --- 4. Результат ---
        lf_output = ttk.LabelFrame(main_frame, text=" 4. Результат ", padding=10)
        lf_output.pack(fill=tk.BOTH, expand=True)

        output_frame = ttk.Frame(lf_output)
        output_frame.pack(fill=tk.BOTH, expand=True)

        out_scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL)
        self.output = tk.Text(output_frame,
                              height=10,
                              yscrollcommand=out_scrollbar.set,
                              font=('Consolas', 10),
                              wrap=tk.WORD)
        out_scrollbar.config(command=self.output.yview)
        out_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.edges = []
        self.from_entry.focus_set()

    # --- Додавання ребра ---
    def add_edge(self):
        u = self.from_entry.get().strip()
        v = self.to_entry.get().strip()
        w = self.weight_entry.get().strip()

        if not u or not v or not w:
            messagebox.showwarning("Увага", "Заповніть усі поля!")
            return

        if u == v:
            messagebox.showerror("Помилка", "Початкова і кінцева вершини не можуть бути однаковими.")
            return

        try:
            if u.lstrip('-').isdigit() and int(u) < 0:
                messagebox.showerror("Помилка", f"Вершина '{u}' не може бути від’ємною.")
                return
            if v.lstrip('-').isdigit() and int(v) < 0:
                messagebox.showerror("Помилка", f"Вершина '{v}' не може бути від’ємною.")
                return
        except ValueError:
            pass

        try:
            w = float(w)
            if w <= 0:
                messagebox.showerror("Помилка", "Вага ребра має бути додатною (> 0).")
                return
        except ValueError:
            messagebox.showerror("Помилка", "Вага має бути числом.")
            return

        self.edges.append((u, v, w))
        self.edges_listbox.insert(tk.END, f"{u} -- {v} (вага={w})")

        self.from_entry.delete(0, tk.END)
        self.to_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.from_entry.focus_set()

    # --- Видалення ребра ---
    def remove_edge(self):
        sel = self.edges_listbox.curselection()
        if sel:
            index = sel[0]
            self.edges.pop(index)
            self.edges_listbox.delete(index)

    # --- Пошук шляхів ---
    def on_submit(self):
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        try:
            K = int(self.k_entry.get().strip())
            if K <= 0:
                messagebox.showerror("Помилка", "K має бути додатним числом (> 0).")
                return
        except ValueError:
            messagebox.showerror("Помилка", "K має бути числом.")
            return

        if not start or not end:
            messagebox.showwarning("Увага", "Введіть початкову та кінцеву вершини.")
            return

        try:
            if start.lstrip('-').isdigit() and int(start) < 0:
                messagebox.showerror("Помилка", f"Початкова вершина '{start}' не може бути від’ємною.")
                return
            if end.lstrip('-').isdigit() and int(end) < 0:
                messagebox.showerror("Помилка", f"Кінцева вершина '{end}' не може бути від’ємною.")
                return
        except ValueError:
            pass

        vertices = set()
        for u, v, _ in self.edges:
            vertices.add(u)
            vertices.add(v)

        if start not in vertices:
            messagebox.showerror("Помилка", f"Початкової точки '{start}' немає в графі.")
            return

        if end not in vertices:
            messagebox.showerror("Помилка", f"Кінцевої точки '{end}' немає в графі.")
            return

        try:
            result = self.callback_paths(self.edges, start, end, K)
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"--- {K} найкоротших шляхів з {start} в {end} ---\n\n")
            if not result:
                self.output.insert(tk.END, "Шляхи не знайдено.\n")
            else:
                for i, (cost, path) in enumerate(result, start=1):
                    self.output.insert(tk.END, f"{i}-й шлях: {' -- '.join(path)}\n   Довжина = {cost}\n")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    # --- Пошук циклів ---
    def on_find_cycles(self):
        if not self.edges:
            messagebox.showwarning("Увага", "Додайте хоча б одне ребро, щоб знайти цикли.")
            return

        try:
            cycles = self.callback_cycles(self.edges)
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"--- Знайдені цикли в графі ---\n\n")
            if not cycles:
                self.output.insert(tk.END, "Циклів не знайдено.\n")
            else:
                for i, cycle in enumerate(cycles, start=1):
                    path_str = " -> ".join(map(str, cycle)) + " -- " + str(cycle[0])
                    self.output.insert(tk.END, f"{i}-й цикл: {path_str}\n")
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

    def run(self):
        self.root.mainloop()
