# module_10_3.py

# Домашнее задание по теме "Очереди для обмена данными между потоками."

import threading
import queue
import time


# Table - класс для столов, который будет содержать следующие атрибуты:
class Table:
    def __init__(self, number):
        # number(int) - номер стола,
        self.number = number
        # is_busy(bool) - занят стол или нет.
        self.is_busy = False


# Customer - класс (поток) посетителя.
class Customer(threading.Thread):
    def __init__(self, customer_id, cafe):
        super().__init__()
        # Порядковый номер customer_id посетителя в очереди.
        self.customer_id = customer_id
        # Кафе, в котором обслуживают посетителя.
        self.cafe = cafe

    def run(self):
        # Посетитель прибыл.
        print(f"Посетитель номер {self.customer_id} прибыл.")
        # Посетитель поступает в очередь.
        self.cafe.queue.put(self.customer_id)
        # Начинается обслуживание посетителя.
        self.cafe.serve_customer()


# Cafe - класс для симуляции процессов в кафе. Должен содержать следующие атрибуты и методы:
class Cafe:
    def __init__(self, tables):
        # Атрибуты queue - очередь посетителей (создаётся внутри init),
        self.queue = queue.Queue()
        # tables список столов (поступает из вне).
        self.tables = tables
        # Используем threading.Lock, чтобы операции с очередью и столиками были безопасными.
        self.lock = threading.Lock()
        # Количество пришедших посетителей.
        self.customer_count = 0
        # Максимальное количество - 20 посетителей.
        self.max_customers = 20

    # Метод customer_arrival(self) - моделирует приход посетителя(каждую секунду).
    def customer_arrival(self):
        # 20 посетителей (ограничение выставить в методе customer_arrival)
        for _ in range(self.max_customers):
            # Моделируем приход нового посетителя.
            self.customer_count += 1
            # Создаем каждому посетителю поток для обработки
            customer_thread = Customer(self.customer_count, self)
            # Запускаем поток
            customer_thread.start()
            # Приход посетителя(каждую секунду).
            time.sleep(1)

    # Создаём функцию find_free_table, чтобы найти свободный стол.
    def find_free_table(self):
        # Для каждого из столов:
        for table in self.tables:
            # Если стол не занят,
            if not table.is_busy:
                # то возвращаем стол.
                return table
        # Возвращаем None
        return None

    # Метод serve_customer(self, customer) - моделирует обслуживание посетителя.
    # Проверяет наличие свободных столов,
    # в случае наличия стола - начинает обслуживание посетителя (запуск потока),
    # в противном случае - посетитель поступает в очередь. Время обслуживания 5 секунд.
    def serve_customer(self):
        while True:
            # Используем Lock
            with self.lock:
                # Если очередь не пустая:
                if not self.queue.empty():
                    # Создаём customer_id посетителя для обслуживания из очереди queue.
                    customer_id = self.queue.queue[0]  # Получаем первого в очереди, но не удаляем
                    # Используем свободный стол.
                    table = self.find_free_table()
                    # Если есть свободный стол:
                    if table:
                        # Сообщаем, что посетитель номер {customer_id} сел за стол {table.number}.
                        print(f"Посетитель номер {customer_id} сел за стол {table.number}.")
                        # Стол занят.
                        table.is_busy = True
                        # Удаляем посетителя из очереди
                        self.queue.get()
                        # Начинаем обслуживание клиента с customer_id за столом - table.
                        self.start_serving(customer_id, table)
                    else:
                        print(f"Посетитель номер {customer_id} ожидает свободный стол.")
                        break
                else:
                    break

    # Функция обслуживания клиента с customer_id за столом - table.
    def start_serving(self, customer_id, table):
        # Запускаем поток для обслуживания посетителя
        threading.Thread(target=self.complete_serving, args=(customer_id, table)).start()

    # Функция завершающая обслуживание посетителя.
    def complete_serving(self, customer_id, table):
        # Время обслуживания 5 секунд.
        time.sleep(5)
        print(f"Посетитель номер {customer_id} покушал и ушёл.")
        with self.lock:
            # Освобождаем стол
            table.is_busy = False
        # Проверяем, есть ли еще посетители в очереди
        self.serve_customer()


# Пример работы:
# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()

# Вывод на консоль (20 посетителей [ограничение выставить в методе customer_arrival]):
# Посетитель номер 1 прибыл
# Посетитель номер 1 сел за стол 1
# Посетитель номер 2 прибыл
# Посетитель номер 2 сел за стол 2
# Посетитель номер 3 прибыл
# Посетитель номер 3 сел за стол 3
# Посетитель номер 4 прибыл
# Посетитель номер 4 ожидает свободный стол
# Посетитель номер 5 прибыл
# Посетитель номер 5 ожидает свободный стол
# ......
# Посетитель номер 20 прибыл
# Посетитель номер 20 ожидает свободный стол
# Посетитель номер 17 покушал и ушёл.
# Посетитель номер 20 сел за стол N.
# Посетитель номер 18 покушал и ушёл.
# Посетитель номер 19 покушал и ушёл.
# Посетитель номер 20 покушал и ушёл.
