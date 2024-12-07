import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import PhotoImage
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
import sqlite3
import os
from ttkthemes import ThemedTk
from time import strftime

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note-Taking App")
        self.root.geometry("600x400")
        self.theme = ttk.Style()
        # clam', 'alt', 'default', 'classic')
        self.theme.theme_use('alt')
        self.root.option_add("*Font", ("Calibri, 11"))
        self.main_color = '#b0d3bf'
        self.dop_color = '#d3e3b6'
        self.root.config(bg=self.main_color)
        
        self.db_file = "notes.db"
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        
        self.create_table()
        self.create_widgets()
        self.load_notes()
    
    def create_table(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS notes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT,
                            category TEXT,
                            content TEXT,
                            create_data TEXT,
                            modified_data TEXT
                            )''')
        self.conn.commit()
    
    def create_widgets(self):
        self.root.title("NoteApp")
        self.root.geometry("800x500")

        # Верхняя панель
        if True:
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

        # Выпадающий список для категорий
        category_label = tk.Label(self.root, text="Show Category:", bg=self.main_color, anchor='e')
        category_label.grid(row=0, column=0, padx=(10, 10), pady=(10), sticky="e") #, sticky="w"
        
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(self.root, textvariable=self.category_var)
        category_combo['values'] = ("All", "Work", "Personal")
        category_combo.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        category_combo.current(0)

        # Список заметок 
        self.note_listbox = tk.Listbox(self.root, width=40, bg=self.dop_color, relief='flat') # selectbackground='#defefe' - Заливка выбранного элемента
        self.note_listbox.grid(row=1, column=0, rowspan=4, padx=10, pady=10, ipadx=10, ipady=10, sticky="nsew")
        self.note_listbox.bind("<<ListboxSelect>>", self.on_note_select)

        # Детали заметки
        self.note_title_label = tk.Label(self.root, text="", font=("Arial", 14), bg=self.main_color)
        self.note_title_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        category_bar = tk.Frame(self.root, bg=self.main_color)
        self.category_label = tk.Label(category_bar, text="Category: ", bg=self.main_color)
        self.category_label.grid(row=0, column=0, sticky="w")
        
        self.category = tk.Label(category_bar, text="", anchor='w', width=42, bg=self.main_color)
        self.category.grid(row=0, column=1, padx=2, sticky="w")
        category_bar.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10)


        timebar = tk.Frame(self.root, bg=self.main_color)
        self.created_label = tk.Label(timebar, text="Created: ", bg=self.main_color)
        self.created_label.grid(row=0, column=0, padx=2, sticky="w")
        
        self.created_time = tk.Label(timebar, text="", anchor='w', width=10, bg=self.main_color)
        self.created_time.grid(row=0, column=1, padx=2, sticky="w")

        self.modified_label = tk.Label(timebar, text="Modified: ", bg=self.main_color)
        self.modified_label.grid(row=0, column=2, padx=(30, 0), sticky="w")
        
        self.modified_time = tk.Label(timebar, text="", anchor='w', width=10, background=self.main_color)
        self.modified_time.grid(row=0, column=3, padx=2, sticky="w")

        timebar.grid(row=3, column=1, columnspan=2, sticky="ew", padx=10, pady=10)
        

        # Прокручиваемое текстовое поле для содержания заметки
        self.note_text = tk.Text(self.root, wrap=tk.WORD, bg=self.dop_color)
        self.note_text.grid(row=4, column=1, columnspan=4, rowspan=2, padx=(10, 20), pady=10, sticky="nsew")

        # Настройка сетки
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(4, weight=1)

        # Панель инструментов (кнопки внизу)
        self.new_icon = PhotoImage(file=r"Sources\Images\add.png", height=30)
        self.edite_icon = PhotoImage(file=r"Sources\Images\edit.png", height=30)
        self.delete_icon = PhotoImage(file=r"Sources\Images\delete.png", height=30)
        
        toolbar = tk.Frame(self.root, width=40, bg=self.main_color)
        new_button = tk.Button(toolbar, text="New", command=self.new_note, image=self.new_icon, bg=self.main_color)
        new_button.pack(side=tk.LEFT, fill='none', padx=20)

        edit_button = tk.Button(toolbar, text="edit", command=self.edit_note, image=self.edite_icon, bg=self.main_color)
        edit_button.pack(side=tk.LEFT, fill='none', padx=20)

        delete_button = tk.Button(toolbar, text="delete", command=self.delete_note, image=self.delete_icon, bg=self.main_color)
        delete_button.pack(side=tk.LEFT, fill='none', padx=20)

        toolbar.grid(row=5, column=0, sticky="ew", padx=10, pady=10)
         
    def delete_note(self):
        # selected_category = self.category_listbox.get(tk.ACTIVE)
        selected_note = self.note_listbox.get(tk.ACTIVE)
        if isinstance(selected_note, (tuple, list)):
            selected_note = selected_note[0]

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
        new_note_window.title("Новая заметка")

        
        tk.Label(new_note_window, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        category_entry = tk.Entry(new_note_window)
        category_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")

        tk.Label(new_note_window, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        title_entry = tk.Entry(new_note_window)
        title_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

        tk.Label(new_note_window, text="Content:").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        content_text = tk.Text(new_note_window, wrap="word", height=10)
        content_text.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")

        
        new_note_window.grid_columnconfigure(1, weight=1)
        new_note_window.grid_rowconfigure(2, weight=1)

        def save_new_note():
            category = category_entry.get()
            title = title_entry.get()
            content = content_text.get(1.0, tk.END)

            if category and title:
                t = strftime('%X')
                self.cursor.execute("INSERT INTO notes (category, title, content, create_data, modified_data) VALUES (?, ?, ?, ?, ?)", 
                                    (category, title, content, t, None))
                self.conn.commit()
                self.load_notes()
                new_note_window.destroy()
                messagebox.showinfo("Success", "New note created.")
            else:
                messagebox.showwarning("Invalid Input", "Category and title are required.")

        save_button = tk.Button(new_note_window, text="Save", command=save_new_note)
        save_button.grid(row=3, column=1, padx=10, pady=5, sticky="e")
        
    def load_notes(self):
        
        # self.category_listbox.delete(0, tk.END)
        self.note_listbox.delete(0, tk.END)

        self.cursor.execute("SELECT DISTINCT title FROM notes")
        headers = self.cursor.fetchall()
        print(headers)

        for header in headers:
            self.note_listbox.insert(tk.END, header[0])

    def edit_note(self):
        selection = self.note_listbox.curselection()
        selected_note = self.note_listbox.get(selection[0])
        if isinstance(selected_note, (tuple, list)):
            selected_note = selected_note[0]
        new_note_window = Toplevel(self.root)
        new_note_window.title("Редактирование заметки")
        
        tk.Label(new_note_window, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        category_entry = tk.Entry(new_note_window)
        category_entry.grid(row=0, column=1, padx=10, pady=5, sticky="we")
        self.cursor.execute(f"SELECT category FROM notes WHERE title = '{selected_note}'")
        category = self.cursor.fetchone()[0]
        category_entry.insert(0, category)

        tk.Label(new_note_window, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        title_entry = tk.Entry(new_note_window)
        title_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")
        # self.cursor.execute(f"SELECT title FROM notes WHERE title = '{selected_note}'")
        # title = self.cursor.fetchone()[0]
        title_entry.insert(0, selected_note)

        tk.Label(new_note_window, text="Content:").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        content_text = tk.Text(new_note_window, wrap="word", height=10)
        content_text.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")
        self.cursor.execute(f"SELECT content FROM notes WHERE title = '{selected_note}'")
        content = self.cursor.fetchone()[0]
        content_text.config(text=content)
        # print(content)
        # content_text.insert(0, content)
        
        new_note_window.grid_columnconfigure(1, weight=1)
        new_note_window.grid_rowconfigure(2, weight=1)

        def update_new_note():
            category = category_entry.get()
            title = title_entry.get()
            content = content_text.get()

            if category and title:
                t = strftime('%X')
                self.cursor.execute("INSERT INTO notes (category, title, content, create_data, modified_data) VALUES (?, ?, ?, ?, ?)", 
                                    (category, title, content, t, None))
                self.conn.commit()
                self.load_notes()
                new_note_window.destroy()
                messagebox.showinfo("Success", "New note created.")
            else:
                messagebox.showwarning("Invalid Input", "Category and title are required.")

        save_button = tk.Button(new_note_window, text="Save", command=update_new_note)
        save_button.grid(row=3, column=1, padx=10, pady=5, sticky="e")
    
    def on_note_select(self, event):
        try:
            selection = self.note_listbox.curselection()
            if selection:
                index = selection[0]
                selected_note = self.note_listbox.get(index)
                if isinstance(selected_note, (tuple, list)):
                    selected_note = selected_note[0]

                self.cursor.execute(f"SELECT title FROM notes WHERE title = '{selected_note}'")
                note_title_label = self.cursor.fetchone()[0]
                
                self.cursor.execute(f"SELECT category FROM notes WHERE title = '{selected_note}'")
                category = self.cursor.fetchone()[0]
                
                self.cursor.execute(f"SELECT create_data FROM notes WHERE title = '{selected_note}'")
                created_time = self.cursor.fetchone()[0]
                
                self.cursor.execute(f"SELECT modified_data FROM notes WHERE title = '{selected_note}'")
                modified_time = self.cursor.fetchone()[0]
                
                self.cursor.execute(f"SELECT content FROM notes WHERE title = '{selected_note}'")
                note_content = self.cursor.fetchone()[0]
                # print(note_title_label, type(note_title_label))
                # print(category, type(category))
                # print(created_time, type(created_time))
                # print(modified_time, type(modified_time))
                
                
                self.note_title_label.config(text=note_title_label)
                self.category.config(text=category)
                self.created_time.config(text=created_time)
                if modified_time is not None:
                    self.modified_time.config(text=modified_time)
                
                self.note_text.delete(1.0, tk.END)
                self.note_text.insert(tk.END, note_content)
                
        except Exception as e:
            print(f"Error selecting note: {e}")
if __name__ == "__main__":
    root = tk.Tk()
    # root = ThemedTk(theme="arc")
    app = NoteApp(root)
    root.mainloop()