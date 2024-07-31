# module_10_5.py

# Домашнее задание по теме "Многопроцессное программирование".
import multiprocessing
import threading


# Создайте класс WarehouseManager - менеджера склада, который будет обладать следующими свойствами:
class WarehouseManager:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        # Атрибут data - словарь, где ключ - название продукта, а значение - его кол-во. (изначально пустой)
        self.data = self.manager.dict()

    # Метод process_request - реализует запрос (действие с товаром), принимая request - кортеж.
    def process_request(self, product, action, quantity):
        # Если действие receipt - получение:
        if action == "receipt":
            # Добавление товара на склад.
            # В случае получения данные должны поступить в data (добавить пару,
            # если её не было и изменить значение ключа, если позиция уже была в словаре).
            # Если продукт есть в словаре, то
            if product in self.data:
                # добавить к уже существующему.
                self.data[product] += quantity
            else:
                # Иначе создать новый ключ product и присвоить ему значение quantity.
                self.data[product] = quantity
        # Если действие shipment - отгрузка.
        elif action == "shipment":
            # Отгрузка товара со склада.
            # В случае отгрузки данные товара должны уменьшаться (если товар есть в data и если товара больше чем 0).
            # Если продукт есть в словаре и в количестве превышающем запрашиваемое, то
            if product in self.data and self.data[product] >= quantity:
                # уменьшить в словаре количество продукта на отгружаемую величину.
                self.data[product] -= quantity

    # Метод run - принимает запросы и создаёт для каждого свой параллельный процесс,
    # запускает его(start) и замораживает(join).
    def run(self, requests):
        self.requests = requests
        processes = []
        for product, action, quantity in requests:
            # Пакет multiprocessing, аналогичный threading, но использующий процессы.
            # process = multiprocessing.Process(target=self.process_request, args=(product, action, quantity))
            process = threading.Thread(target=self.process_request, args=(product, action, quantity))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()


if __name__ == '__main__':
    # Пример работы:
    # Создаем менеджера склада
    manager = WarehouseManager()

    # Множество запросов на изменение данных о складских запасах
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]

    # Запускаем обработку запросов
    manager.run(requests)

    # Выводим обновленные данные о складских запасах
    print(manager.data)

    # Вывод на консоль:
    # {"product1": 70, "product2": 100, "product3": 200}
