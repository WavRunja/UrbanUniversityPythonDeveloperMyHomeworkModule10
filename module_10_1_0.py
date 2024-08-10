# module_10_1_0.py
from datetime import datetime, timedelta
from collections import defaultdict


# Реализуйте систему учета посещений для фитнес-клуба.
# У каждого клиента есть имя, и каждый раз, когда клиент приходит в клуб, его посещение регистрируется.
# Необходимо написать функцию, которая будет возвращать количество посещений клиента, используя замыкание.


# Класс клиент фитнес-клуба.
class Client:
    # Инициализация клиента фитнес-клуба.
    def __init__(self, name):
        # Имя клиента фитнес-клуба.
        self.name = name
        # Количество посещений клиентом фитнес-клуба.
        self.visits = []
        # Услуги предоставляемые фитнес-клубом клиенту.
        self.services = []
        # Сумма, потраченная клиентом в фитнес-клубе.
        self.total_spent = 0
        # Штамп времени.
        self.timestamp = datetime.now()

    # Регистрация посещения клиентом фитнес-клуба.
    def register_visit(self):
        # Добавление времени посещения клиентом фитнес-клуба в список посещений.
        formatted_time = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        self.visits.append(formatted_time)

    # Покупка дополнительной услуги клиентом в фитнес-клубе.
    def purchase_service(self, service_name, price):
        # Учёт услуги, предоставляемой фитнес-клубом клиенту и её стоимости.
        self.services.append((service_name, price))
        # Увеличение суммы, потраченной клиентом в фитнес-клубе на величину стоимости услуги.
        self.total_spent += price

    # Подсчёт количества посещений клиентом фитнес-клуба.
    def visit_count(self):
        # Возврат количества посещений.
        return len(self.visits)

    # Подсчёт количества посещений клиентом фитнес-клуба за указанный, минувший период времени.
    def visits_in_period(self, period_days):
        # Нахождение начала указанного, минувшего периода времени.
        period_start = datetime.now() - timedelta(days=period_days)
        # Возврат количества посещений за указанный, минувший период времени.
        return len([visit for visit in self.visits if visit >= period_start])


# Класс фитнес-клуб, который служит для управления клиентами и их посещениями.
class FitnessClub:
    # Инициализация фитнес-клуба.
    def __init__(self):
        # Множество клиентов фитнес-клуба.
        self.clients = {}
        # Список VIP клиентов фитнес-клуба.
        self.vip_clients = []
        # Прибыль фитнес-клуба.
        self.total_income = 0
        # Регулярные посетители фитнес-клуба.
        self.regular_visitors = defaultdict(int)
        # Пороговое значение суммы расходов для VIP клиента.
        self.threshold_value = 500

    # Добавление клиента фитнес-клуба.
    def add_client(self, name):
        # Если посетитель фитнес-клуба отсутствует в списке клиентов:
        if name not in self.clients:
            # Создание клиента с указанным именем.
            self.clients[name] = Client(name)

    def register_visit(self, name):
        # Если клиент из множества клиентов фитнес-клуба:
        if name in self.clients:
            # Учёт посещения клиентом фитнес-клуба.
            self.clients[name].register_visit()
            # Обновление количества постоянных посетителей
            visits = self.clients[name].visit_count()
            self.regular_visitors[name] = visits
            # Указание посетителя как VIP-клиента, если общая сумма его расходов превышает пороговое значение
            if self.clients[name].total_spent > self.threshold_value:
                # Если клиент фитнес-клуба отсутствует в списке VIP клиентов:
                if name not in self.vip_clients:
                    # Добавление клиента в список VIP клиентов фитнес-клуба.
                    self.vip_clients.append(name)

    # Покупка услуги фитнес-клуба.
    def purchase_service(self, name, service_name, price):
        # Если клиент из множества клиентов фитнес-клуба:
        if name in self.clients:
            # Клиент покупает услугу у фитнес-клуба.
            self.clients[name].purchase_service(service_name, price)
            # Прибыль фитнес-клуба возрастает на величину стоимости услуги.
            self.total_income += price
            # Проверка и обновление VIP-статуса.
            if self.clients[name].total_spent > self.threshold_value and name not in self.vip_clients:
                # Добавление клиента в список VIP клиентов фитнес-клуба.
                self.vip_clients.append(name)

    # Информация о клиенте.
    def client_info(self, name):
        #  Если клиент из множества клиентов фитнес-клуба:
        if name in self.clients:
            client = self.clients[name]
            # То, вернётся информация:
            return {
                # Имя клиента фитнес-клуба.
                'name': client.name,
                # Количество посещений фитнес-клуба.
                'total_visits': client.visit_count(),
                # Сумма, потраченная клиентом в фитнес-клубе.
                'total_spent': client.total_spent,
                # Услуги предоставленные фитнес-клубом клиенту.
                'services': client.services,
                # Количество посещений клиентом фитнес-клуба.
                'visits': client.visits
            }

    # Самые регулярные посетители
    def most_regular_visitors(self):
        # Клиенты, которые посещали фитнес-клуб больше всех.
        return sorted(self.regular_visitors.items(), key=lambda x: x[1], reverse=True)

    # Общая прибыль фитнес-клуба.
    def total_profit(self):
        # Вернётся прибыль фитнес-клуба.
        return self.total_income

    # Информация о VIP-клиентах фитнес-клуба.
    def vip_clients_info(self):
        # Вернётся информации о VIP-клиентах
        return {name: self.client_info(name) for name in self.vip_clients}


# Пример использования:
club = FitnessClub()

# Добавляем клиентов
club.add_client("Дуэйн Джонсон")
club.add_client("Тейлор Свифт")
club.add_client("Вин Дизель")

# Регистрация посещений
club.register_visit("Дуэйн Джонсон")
club.register_visit("Тейлор Свифт")
club.register_visit("Дуэйн Джонсон")
club.register_visit("Вин Дизель")
club.register_visit("Тейлор Свифт")
club.register_visit("Дуэйн Джонсон")
club.register_visit("Вин Дизель")
club.register_visit("Дуэйн Джонсон")
club.register_visit("Тейлор Свифт")

# Покупка услуг
club.purchase_service("Дуэйн Джонсон", "Персональные тренировки", 300)
club.purchase_service("Тейлор Свифт", "Занятия йогой", 100)
club.purchase_service("Вин Дизель", "Абонемент на спортзал", 600)
club.purchase_service("Дуэйн Джонсон", "Занятия йогой", 100)

# Вывод информации о клиенте
print("Информация о клиенте Дуэйн Джонсон:", club.client_info("Дуэйн Джонсон"))
print("VIP клиенты:", club.vip_clients_info())
print("Самые регулярные посетители:", club.most_regular_visitors())

# Общая прибыль фитнес-клуба
print("Общая прибыль клуба:", club.total_profit())
