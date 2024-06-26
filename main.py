import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
import json
from datetime import datetime
from typing import List, Dict, Any

# Файл для сохранения данных
data_file = 'training_log.json'


def load_data() -> List[Dict[str, Any]]:
    """Загрузка данных о тренировках из файла."""
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data: List[Dict[str, Any]]) -> None:
    """Сохранение данных о тренировках в файл."""
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)


class TrainingLogApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Дневник тренировок")
        self.create_widgets()

    def create_widgets(self) -> None:
        # Виджеты для ввода данных
        self.exercise_label = ttk.Label(self.root, text="Упражнение:")
        self.exercise_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.exercise_entry = ttk.Entry(self.root)
        self.exercise_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        self.weight_label = ttk.Label(self.root, text="Вес:")
        self.weight_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        self.repetitions_label = ttk.Label(self.root, text="Повторения:")
        self.repetitions_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.repetitions_entry = ttk.Entry(self.root)
        self.repetitions_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        self.add_button = ttk.Button(self.root, text="Добавить запись", command=self.add_entry)
        self.add_button.grid(column=0, row=3, columnspan=2, pady=10)

        self.view_button = ttk.Button(self.root, text="Просмотреть записи", command=self.view_records)
        self.view_button.grid(column=0, row=4, columnspan=2, pady=10)

        # Виджеты для фильтрации по дате
        self.from_date_label = ttk.Label(self.root, text="С даты (гггг-мм-дд):")
        self.from_date_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

        self.from_date_entry = ttk.Entry(self.root)
        self.from_date_entry.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)

        self.to_date_label = ttk.Label(self.root, text="По дату (гггг-мм-дд):")
        self.to_date_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

        self.to_date_entry = ttk.Entry(self.root)
        self.to_date_entry.grid(column=1, row=6, sticky=tk.EW, padx=5, pady=5)

        self.filter_date_button = ttk.Button(self.root, text="Фильтровать по дате", command=self.filter_records_by_date)
        self.filter_date_button.grid(column=0, row=7, columnspan=2, pady=10)

        # Виджеты для фильтрации по упражнению
        self.filter_exercise_label = ttk.Label(self.root, text="Фильтровать по упражнению:")
        self.filter_exercise_label.grid(column=0, row=8, sticky=tk.W, padx=5, pady=5)

        self.filter_exercise_entry = ttk.Entry(self.root)
        self.filter_exercise_entry.grid(column=1, row=8, sticky=tk.EW, padx=5, pady=5)

        self.filter_exercise_button = ttk.Button(self.root, text="Фильтровать по упражнению", command=self.filter_records_by_exercise)
        self.filter_exercise_button.grid(column=0, row=9, columnspan=2, pady=10)

    def add_entry(self) -> None:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        entry = {
            'date': date,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        data = load_data()
        data.append(entry)
        save_data(data)

        # Очистка полей ввода после добавления
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")

    def view_records(self) -> None:
        data = load_data()
        self.show_records(data)

    def filter_records_by_date(self) -> None:
        """
        Фильтрация записей по дате. Пользователь вводит начальную и конечную даты,
        и отображаются только те записи, которые попадают в этот диапазон.

        Raises:
            ValueError: Если введены даты в неправильном формате.
        """
        from_date_str = self.from_date_entry.get()
        to_date_str = self.to_date_entry.get()

        try:
            from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
            to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте гггг-мм-дд.")
            return

        data = load_data()
        filtered_data = [entry for entry in data if from_date <= datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S') <= to_date]
        self.show_records(filtered_data)

    def filter_records_by_exercise(self) -> None:
        """
        Фильтрация записей по упражнению. Пользователь вводит название упражнения,
        и отображаются только те записи, которые соответствуют этому названию.
        """
        exercise_filter = self.filter_exercise_entry.get().strip().lower()
        if not exercise_filter:
            messagebox.showerror("Ошибка", "Введите название упражнения для фильтрации!")
            return

        data = load_data()
        filtered_data = [entry for entry in data if entry['exercise'].strip().lower() == exercise_filter]
        self.show_records(filtered_data)

    def show_records(self, data: List[Dict[str, Any]]) -> None:
        """
        Отображение записей в новом окне. Создается новое окно с таблицей,
        в которой перечислены все записи.

        Args:
            data (List[Dict[str, Any]]): Список записей для отображения.
        """
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")

        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")

        for entry in data:
            tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))

        tree.pack(expand=True, fill=tk.BOTH)


def main() -> None:
    root = tk.Tk()
    TrainingLogApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
