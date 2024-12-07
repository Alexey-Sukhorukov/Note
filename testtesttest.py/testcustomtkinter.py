import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import sqlite3

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note-Taking App")
        self.root.geometry("800x500")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.db_file = "notes.db"
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

        self.create_table()
        self.create_widgets()
        self.load_notes()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT,
                                category TEXT,
                                content TEXT,
                                create_data TEXT,
                                modified_data TEXT)''')
        self.conn.commit()

    def create_widgets(self):
        # Меню
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Add Note", command=self.new_note)
        file_menu.add_command(label="Edit Note", command=self.edit_note)
        file_menu.add_command(label="Remove Note", command=self.delete_note)
        menubar.add_cascade(label="File", menu=file_menu)

        exit_menu = tk.Menu(menubar, tearoff=0)
        exit_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Edit", menu=exit_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

        # Виджеты для категорий
        category_combo_bar = ctk.CTkFrame(self.root)
        category_label = ctk.CTkLabel(category_combo_bar, text="Show Category:")
        category_label.grid(row=0, column=0, padx=(10, 10), pady=(10), sticky="e")

        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(category_combo_bar, textvariable=self.category_var, validate='key')
        self.cursor.execute(f"SELECT DISTINCT category FROM notes")
        all_categories = self.cursor.fetchall()
        self.category_combo['values'] = tuple(all_categories)
        self.category_combo.grid(row=0, column=1, padx=(5, 5), pady=10, sticky="we")
        self.category_combo.current(0)
        category_combo_bar.grid(column=0, row=0, sticky="nsew")

        # Список заметок
        self.note_listbox = ttk.Treeview(self.root, show="tree")
        self.note_listbox.grid(row=1, column=0, rowspan=4, padx=10, pady=(10, 0), sticky="nsew")
        self.note_listbox.bind("<<TreeviewSelect>>", self.on_note_select)

        # Детали заметки
        self.note_title_label = ctk.CTkLabel(self.root, text="", font=("Arial", 14))
        self.note_title_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        category_bar = ctk.CTkFrame(self.root)
        self.category_label = ctk.CTkLabel(category_bar, text="Category: ")
        self.category_label.grid(row=0, column=0, sticky="w")

        self.category = ctk.CTkLabel(category_bar, text="", anchor='w', width=42)
        self.category.grid(row=0, column=1, padx=2, sticky="w")
        category_bar.grid(row=1, column=1, columnspan=2, sticky="ew", padx=10)

        # Дата создания и изменения
        timebar = ctk.CTkFrame(self.root)
        self.created_label = ctk.CTkLabel(timebar, text="Created: ")
        self.created_label.grid(row=0, column=0, padx=2, sticky="w")

        self.created_time = ctk.CTkLabel(timebar, text="", anchor='w', width=20)
        self.created_time.grid(row=0, column=1, padx=2, sticky="w")

        self.modified_label = ctk.CTkLabel(timebar, text="Modified: ")
        self.modified_label.grid(row=0, column=2, padx=(20, 0), sticky="w")

        self.modified_time = ctk.CTkLabel(timebar, text="", anchor='w', width=10)
        self.modified_time.grid(row=0, column=3, padx=2, sticky="w")

        timebar.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10, pady=10)

        # Прокручиваемое текстовое поле для содержания заметки
        text_frame = ctk.CTkFrame(self.root)
        text_frame.grid(row=3, column=1, columnspan=4, rowspan=3, padx=(10, 20), pady=(5, 5), sticky="nsew")
        self.note_text = ctk.CTkTextbox(text_frame, wrap=tk.WORD, undo=True)
        self.note_text.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # Настройка сетки
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

        # Панель инструментов
        toolbar = ctk.CTkFrame(self.root)
        new_button = ctk.CTkButton(toolbar, text="New", command=self.new_note)
        new_button.pack(side=tk.LEFT, fill='none', padx=20)

        edit_button = ctk.CTkButton(toolbar, text="Edit", command=self.edit_note)
        edit_button.pack(side=tk.LEFT, fill='none', padx=20)

        delete_button = ctk.CTkButton(toolbar, text="Delete", command=self.delete_note)
        delete_button.pack(side=tk.LEFT, fill='none', padx=20)

        toolbar.grid(row=5, column=0, sticky="ew", padx=10, pady=(5, 5))
        
    def delete_note(self):
        selected_note = self.note_listbox.get(tk.ACTIVE)
        if selected_note:
            self.cursor.execute(f"DELETE FROM notes WHERE title = '{selected_note}'")
            self.conn.commit()
            self.load_notes()
            self.note_text.delete(1.0, tk.END)
            messagebox.showinfo("Success", "Note deleted successfully.")
        else:
            messagebox.showwarning("No Note Selected", "Please select a note to delete.")

    def new_note(self):
        new_note_window = Toplevel(self.root)
        new_note_window.title("New Note")

        ttk.Label(new_note_window, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        category_entry = ttk.Entry(new_note_window)
        category_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(new_note_window, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        title_entry = ttk.Entry(new_note_window)
        title_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        ttk.Label(new_note_window, text="Content:").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        content_text = tk.Text(new_note_window, wrap="word", height=10, undo=True, maxundo=5000)
        content_text.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

        new_note_window.grid_columnconfigure(1, weight=1)
        new_note_window.grid_rowconfigure(2, weight=1)

        def save_new_note():
            category = category_entry.get()
            title = title_entry.get()
            content = content_text.get(1.0, tk.END)

            if category and title:
                t = f"{strftime('%X')}  {strftime('%D')}"
                print(t)
                self.cursor.execute("INSERT INTO notes (category, title, content, create_data, modified_data) VALUES (?, ?, ?, ?, ?)", 
                                    (category, title, content, t, None))
                self.conn.commit()
                self.load_notes()
                new_note_window.destroy()
                messagebox.showinfo("Success", "New note created.")
            else:
                messagebox.showwarning("Invalid Input", "Category and title are required.")

        save_button = ttk.Button(new_note_window, text="Save", command=save_new_note)
        save_button.grid(row=3, column=1, padx=10, pady=5, sticky="e")

    def load_notes(self):
        # self.note_listbox.delete(0, tk.END)
        for row in self.note_listbox.get_children():
            self.note_listbox.delete(row)
        self.cursor.execute("SELECT DISTINCT title FROM notes")
        headers = self.cursor.fetchall()

        for idx, header in enumerate(headers):
            # self.note_listbox.insert(tk.END, header[0])
            # print(header[0])
            self.note_listbox.insert("", tk.END, text=header[0])

    def edit_note(self):
        selection = self.note_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Note Selected", "Please select a note to edit.")
            return

        selected_note = self.note_listbox.get(selection[0])

        # Окно для редактирования заметки
        edit_note_window = Toplevel(self.root)
        edit_note_window.title("Edit Note")

        # Поле для редактирования категории
        ttk.Label(edit_note_window, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        category_entry = ttk.Entry(edit_note_window)
        category_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")
        self.cursor.execute(f"SELECT category FROM notes WHERE title = ?", (selected_note,))
        category = self.cursor.fetchone()[0]
        category_entry.insert(0, category)

        # Поле для редактирования заголовка
        ttk.Label(edit_note_window, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        title_entry = ttk.Entry(edit_note_window)
        title_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")
        title_entry.insert(0, selected_note)

        # Поле для редактирования содержания
        ttk.Label(edit_note_window, text="Content:").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        content_text = scrolledtext.ScrolledText(edit_note_window, wrap="word", height=10)
        content_text.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")
        self.cursor.execute(f"SELECT content FROM notes WHERE title = ?", (selected_note,))
        content = self.cursor.fetchone()[0]
        content_text.insert(tk.END, content)

        # Настройка сетки для окна редактирования
        edit_note_window.grid_columnconfigure(1, weight=1)
        edit_note_window.grid_rowconfigure(2, weight=1)

        # Функция сохранения изменений
        def save_edited_note():
            new_category = category_entry.get()
            new_title = title_entry.get()
            new_content = content_text.get(1.0, tk.END).strip()

            if new_category and new_title:
                t = f"{strftime('%X')}  {strftime('%D')}"
                self.cursor.execute(
                    "UPDATE notes SET category = ?, title = ?, content = ?, modified_data = ? WHERE title = ?",
                    (new_category, new_title, new_content, t, selected_note)
                )
                self.conn.commit()
                self.load_notes()
                edit_note_window.destroy()
                messagebox.showinfo("Success", "Note updated successfully.")
            else:
                messagebox.showwarning("Invalid Input", "Category and title cannot be empty.")

        # Кнопка для сохранения изменений
        save_button = ttk.Button(edit_note_window, text="Save", command=save_edited_note)
        save_button.grid(row=3, column=1, padx=10, pady=5, sticky="e")


    def on_note_select(self, event):
        try:
            # selection = self.note_listbox.curselection()
            # if selection:
            if True:
                selected_item = self.note_listbox.selection()[0]  # Получаем выбранный элемент
                selected_note = self.note_listbox.item(selected_item, 'text')  # Достаем данные элемента
                # selected_note = note_data[0]
                # index = selection[0]
                # selected_note = self.note_listbox.get(index)
                # selected_note = note_data = self.note_listbox.item(selected_item, 'values')

                self.cursor.execute(f"SELECT title FROM notes WHERE title = '{selected_note}'")
                note_title_label = self.cursor.fetchone()[0]

                self.cursor.execute(f"SELECT category FROM notes WHERE title = '{selected_note}'")
                category = self.cursor.fetchone()[0]

                self.cursor.execute(f"SELECT content FROM notes WHERE title = '{selected_note}'")
                content = self.cursor.fetchone()[0]

                self.cursor.execute(f"SELECT create_data FROM notes WHERE title = '{selected_note}'")
                create_data = self.cursor.fetchone()[0]

                self.cursor.execute(f"SELECT modified_data FROM notes WHERE title = '{selected_note}'")
                modified_data = self.cursor.fetchone()[0]

                self.note_title_label.config(text=note_title_label)
                self.note_text.delete(1.0, tk.END)
                self.note_text.insert(tk.END, content)
                self.category.config(text=category)
                self.created_time.config(text=create_data)
                self.modified_time.config(text=modified_data)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = NoteApp(root)
    root.mainloop()
