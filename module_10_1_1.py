# module_10_1_1.py

from datetime import datetime, timedelta
# Задача: "Приложение-заметки".

# Реализуйте приложение-заметки. Основной функционал: внесение заметки, вывод всех заметок.
# Далее этот функционал совершенствовать:
# добавить к заметкам время их создания,
# приоритет важности,
# добавить вывод с фильтрацией по времени,
# по важности.
# Добавить разделы для заметок.

# Класс заметка.
class Note:
    # Инициализация заметки.
    def __init__(self, content, priority=1, section="Общие заметки"):
        # Функционал: содержание заметки.
        self.content = content
        # Функционал: время создания.
        self.timestamp = datetime.now()
        # Функционал: приоритет важности.
        self.priority = priority
        # Функционал: раздел для заметок.
        self.section = section

    # Основной функционал: вывод строкового представления заметки.
    def __str__(self):
        formatted_time = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{formatted_time}] [{self.section}] (Приоритет: {self.priority}) {self.content}"


# Класс приложение-заметки.
class NotesApp:
    def __init__(self):
        # Добавляем пустой список заметок.
        self.notes = []

    # Основной функционал: внесение заметки.
    def add_note(self, content, priority=1, section="General"):
        # Добавляем заметку.
        note = Note(content, priority, section)
        # Вносим её в список заметок.
        self.notes.append(note)

    # Основной функционал: вывод всех заметок.
    def show_notes(self, filter_by=None, value=None):
        # Добавляем список заметок в отфильтрованные заметки.
        filtered_notes = self.notes

        # Добавляем вывод с фильтрацией по времени, по важности.
        # По важности:
        if filter_by == "priority":
            filtered_notes = [note for note in self.notes if note.priority == value]
        # По времени:
        elif filter_by == "time":
            filtered_notes = [note for note in self.notes if note.timestamp >= value]
        # По разделам:
        elif filter_by == "section":
            filtered_notes = [note for note in self.notes if note.section == value]

        # Выводим отфильтрованные заметки
        for note in filtered_notes:
            print(note)


# Пример использования

# Создаем приложение для заметок
app = NotesApp()

# Добавляем заметки
app.add_note("Покупка продуктов", priority=2, section="Личные")
app.add_note("Крайний срок публикации релиза", priority=1, section="Рабочие")
app.add_note("План поездок", priority=3, section="Путешествия")

# Вывод всех заметок
print("Все заметки:")
app.show_notes()

# Фильтрация по приоритету важности
print("\nЗаметки с приоритетом 1:")
app.show_notes(filter_by="priority", value=1)

# Фильтрация по времени (например, последние 5 минут)
print("\nЗаметки, добавленные за последние 5 минут:")
time_filter = datetime.now() - timedelta(minutes=5)
app.show_notes(filter_by="time", value=time_filter)

# Фильтрация по разделу
print("\nЗаметки в разделе 'Рабочие':")
app.show_notes(filter_by="section", value="Рабочие")
