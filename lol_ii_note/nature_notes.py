import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import json
from datetime import datetime
from PIL import Image, ImageTk
import webbrowser

class NatureNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Природные заметки")
        self.root.geometry("800x600")
        self.root.configure(bg="#e8f5e9")
        
        # Создаем папку для заметок, если ее нет
        self.notes_dir = "nature_notes"
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)
        
        # Загружаем иконки природы
        self.load_nature_icons()
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Загружаем список заметок
        self.load_notes_list()
    
    def load_nature_icons(self):
        try:
            # Здесь должны быть пути к вашим изображениям
            # Для примера используем стандартные иконки, но с зелеными цветами
            self.tree_icon = self.create_colored_icon("🌳", "#2e7d32")
            self.leaf_icon = self.create_colored_icon("🍃", "#388e3c")
            self.flower_icon = self.create_colored_icon("🌸", "#d81b60")
            self.bird_icon = self.create_colored_icon("🐦", "#1976d2")
        except:
            # Если иконки не загрузились, используем текстовые метки
            self.tree_icon = "🌳"
            self.leaf_icon = "🍃"
            self.flower_icon = "🌸"
            self.bird_icon = "🐦"
    
    def create_colored_icon(self, text, color):
        # Создаем цветную иконку из текстового символа
        image = Image.new('RGBA', (30, 30), (0, 0, 0, 0))
        return image  # В реальном приложении нужно добавить текст на изображение
    
    def create_widgets(self):
        # Стиль для элементов интерфейса
        style = ttk.Style()
        style.configure("Nature.TFrame", background="#e8f5e9")
        style.configure("Nature.TLabel", background="#e8f5e9", foreground="#2e7d32", font=('Helvetica', 10))
        style.configure("Nature.TButton", background="#81c784", foreground="#1b5e20", font=('Helvetica', 10))
        style.map("Nature.TButton", background=[('active', '#66bb6a')])
        
        # Главный фрейм
        main_frame = ttk.Frame(self.root, style="Nature.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель - список заметок
        left_panel = ttk.Frame(main_frame, style="Nature.TFrame", width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        ttk.Label(left_panel, text="Мои природные заметки", style="Nature.TLabel", 
                 font=('Helvetica', 12, 'bold')).pack(pady=(0, 10))
        
        # Кнопки управления
        btn_frame = ttk.Frame(left_panel, style="Nature.TFrame")
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Новая заметка", command=self.new_note, 
                  style="Nature.TButton", image=self.flower_icon, compound=tk.LEFT).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Удалить заметку", command=self.delete_note, 
                  style="Nature.TButton", image=self.leaf_icon, compound=tk.LEFT).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Сохранить", command=self.save_note, 
                  style="Nature.TButton", image=self.tree_icon, compound=tk.LEFT).pack(fill=tk.X, pady=2)
        
        # Список заметок
        self.notes_list = tk.Listbox(left_panel, bg="#c8e6c9", fg="#1b5e20", 
                                    selectbackground="#81c784", font=('Helvetica', 10))
        self.notes_list.pack(fill=tk.BOTH, expand=True)
        self.notes_list.bind('<<ListboxSelect>>', self.load_note)
        
        # Правая панель - просмотр и редактирование заметки
        right_panel = ttk.Frame(main_frame, style="Nature.TFrame")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Поле для названия заметки
        ttk.Label(right_panel, text="Название заметки:", style="Nature.TLabel").pack(anchor=tk.W)
        self.title_entry = ttk.Entry(right_panel, font=('Helvetica', 12))
        self.title_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Поле для текста заметки
        ttk.Label(right_panel, text="Текст заметки:", style="Nature.TLabel").pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD, 
                                                     bg="#f1f8e9", fg="#1b5e20", 
                                                     font=('Helvetica', 11), padx=5, pady=5)
        self.content_text.pack(fill=tk.BOTH, expand=True)
        
        # Статус бар
        self.status_bar = ttk.Label(self.root, text="Готово", relief=tk.SUNKEN, 
                                  anchor=tk.W, style="Nature.TLabel")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)
        
        # Меню
        self.create_menu()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0, bg="#e8f5e9", fg="#2e7d32")
        file_menu.add_command(label="Новая заметка", command=self.new_note, accelerator="Ctrl+N")
        file_menu.add_command(label="Сохранить", command=self.save_note, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0, bg="#e8f5e9", fg="#2e7d32")
        help_menu.add_command(label="О программе", command=self.about)
        help_menu.add_command(label="Советы по природе", command=self.nature_tips)
        menubar.add_cascade(label="Справка", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # Горячие клавиши
        self.root.bind('<Control-n>', lambda e: self.new_note())
        self.root.bind('<Control-s>', lambda e: self.save_note())
    
    def load_notes_list(self):
        self.notes_list.delete(0, tk.END)
        try:
            notes = os.listdir(self.notes_dir)
            for note in notes:
                if note.endswith('.json'):
                    self.notes_list.insert(tk.END, note[:-5])
        except Exception as e:
            self.show_status(f"Ошибка загрузки списка заметок: {str(e)}")
    
    def new_note(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete(1.0, tk.END)
        self.show_status("Создается новая заметка...")
    
    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        
        if not title:
            messagebox.showwarning("Предупреждение", "Введите название заметки")
            return
        
        note_data = {
            "title": title,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            with open(os.path.join(self.notes_dir, f"{title}.json"), 'w', encoding='utf-8') as f:
                json.dump(note_data, f, ensure_ascii=False, indent=2)
            self.show_status(f"Заметка '{title}' сохранена")
            self.load_notes_list()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить заметку: {str(e)}")
    
    def load_note(self, event=None):
        try:
            selected = self.notes_list.curselection()
            if not selected:
                return
            
            title = self.notes_list.get(selected[0])
            with open(os.path.join(self.notes_dir, f"{title}.json"), 'r', encoding='utf-8') as f:
                note_data = json.load(f)
            
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, note_data["title"])
            self.content_text.delete(1.0, tk.END)
            self.content_text.insert(1.0, note_data["content"])
            self.show_status(f"Загружена заметка '{title}'")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заметку: {str(e)}")
    
    def delete_note(self):
        selected = self.notes_list.curselection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите заметку для удаления")
            return
        
        title = self.notes_list.get(selected[0])
        if messagebox.askyesno("Подтверждение", f"Удалить заметку '{title}'?"):
            try:
                os.remove(os.path.join(self.notes_dir, f"{title}.json"))
                self.show_status(f"Заметка '{title}' удалена")
                self.load_notes_list()
                self.new_note()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить заметку: {str(e)}")
    
    def about(self):
        about_text = """Природные заметки v1.0

Простое приложение для записи ваших наблюдений за природой.
Сохраняйте свои мысли, идеи и наблюдения в этом удобном приложении.

Используйте его как дневник природы, записную книжку натуралиста
или просто для хранения важных мыслей в стиле природы."""
        
        messagebox.showinfo("О программе", about_text)
    
    def nature_tips(self):
        webbrowser.open("https://www.nature.org/en-us/about-us/who-we-are/our-science/nature-tips/")
    
    def show_status(self, message):
        self.status_bar.config(text=message)
        self.root.after(5000, lambda: self.status_bar.config(text="Готово"))

if __name__ == "__main__":
    root = tk.Tk()
    app = NatureNotesApp(root)
    root.mainloop()