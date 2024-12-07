import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Treeview с одним столбцом и без заголовка
tree = ttk.Treeview(root, columns=("col1"), show="tree")
tree.pack(fill=tk.BOTH, expand=True)

# Добавление элементов в первый столбец
tree.insert("", "end", text="Note 1")
tree.insert("", "end", text="Note 2")
tree.insert("", "end", text="Note 3")

root.mainloop()