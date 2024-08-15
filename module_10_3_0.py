# module_10_3.py

# Задача "Банковские операции".

import threading
import random
import time


# Необходимо создать класс Bank со следующими свойствами:
class Bank:
    def __init__(self):
        # Атрибуты объекта:
        # balance - баланс банка (int)
        self.balance = 0
        # lock - объект класса Lock для блокировки потоков.
        self.lock = threading.Lock()
        # Класс Condition, реализующий переменную условия.
        # Переменная условия позволяет одному или нескольким потокам ожидать, пока они не будут
        # уведомлены другим потоком.
        # Если аргумент блокировки указан и не None, это должен быть объект Lock или RLock,
        # и он используется как базовая блокировка. В противном случае создается новый объект RLock,
        # который используется как базовая блокировка.
        self.condition = threading.Condition(self.lock)

    # Методы объекта:
    # Метод deposit:
    def deposit(self):
        # 1. Будет совершать 100 транзакций пополнения средств.
        for _ in range(100):
            # 2. Пополнение - это увеличение баланса на случайное целое число от 50 до 500.
            amount = random.randint(50, 500)
            # print(f'{_ + 1} транзакция пополнения средств.')
            with self.lock:
                # 3. Если баланс больше или равен 500 и замок lock заблокирован - lock.locked(),
                if self.balance >= 500 and self.lock.locked():
                    # то разблокировать его методом release.
                    # self.lock.release()

                    # Release: Освободите блокировку, уменьшив уровень рекурсии.
                    # Если после декремента он равен нулю, сбросьте блокировку до разблокированной
                    # (не принадлежит ни одному потоку), и если какие-либо другие потоки заблокированы, ожидая,
                    # чтобы разблокировать блокировку, разрешите продолжить работу ровно одному из них. Если после
                    # декремента уровень рекурсии все еще не равен нулю, блокировка остается
                    # заблокированной и принадлежит вызывающему потоку.
                    # Вызывайте этот метод только тогда, когда вызывающий поток владеет блокировкой. Возникает
                    # RuntimeError, если этот метод вызывается, когда блокировка разблокирована.
                    # Возвращаемого значения нет.

                    # Разбудить все потоки, ожидающие этого условия.
                    # Если вызывающий поток не получил блокировку при вызове этого метода,
                    # возникает ошибка RuntimeError.
                    self.condition.notify_all()
                self.balance += amount
                # 4. После увеличения баланса должна выводится строка "Пополнение: <случайное число>.
                # Баланс: <текущий баланс>".
                print(f"Пополнение: {amount}. Баланс: {self.balance}")
            # 5. Также после всех операций поставьте ожидание в 0.001 секунды,
            # тем самым имитируя скорость выполнения пополнения.
            time.sleep(0.001)

    # Метод take:
    def take(self):
        # 1. Будет совершать 100 транзакций снятия.
        for _ in range(100):
            # 2. Снятие - это уменьшение баланса на случайное целое число от 50 до 500.
            amount = random.randint(50, 500)
            # print(f'{_ + 1} транзакция снятия средств.')
            with self.lock:
                # 3. В начале должно выводится сообщение "Запрос на <случайное число>".
                print(f"Запрос на {amount}")
                # 4. Далее производится проверка: если случайное число меньше или равно текущему балансу,
                if amount <= self.balance:
                    # то произвести снятие, уменьшив balance на соответствующее число
                    self.balance -= amount
                    # и вывести на экран "Снятие: <случайное число>. Баланс: <текущий баланс>".
                    print(f"Снятие: {amount}. Баланс: {self.balance}")
                # 5. Если случайное число оказалось больше баланса,
                else:
                    # то вывести строку "Запрос отклонён, недостаточно средств"
                    print("Запрос отклонён, недостаточно средств")
                    # и заблокировать поток методом acquiere.
                    # self.lock.acquire()

                    # wait()
                    # Ожидайте уведомления или истечения времени ожидания.
                    #
                    # Если вызывающий поток не получил блокировку при вызове этого метода, возникает ошибка
                    # RuntimeError.
                    #
                    # Этот метод снимает базовую блокировку, а затем блокируется до тех пор, пока она не будет
                    # разбужена вызовом notify() или notify_all() для той же переменной условия
                    # в другом потоке или пока не наступит необязательный тайм-аут. После
                    # разбужения или истечения времени ожидания он повторно получает блокировку и возвращается.
                    #
                    # Если аргумент timeout присутствует и не равен None, он должен быть
                    # числом с плавающей точкой, указывающим время ожидания для операции в секундах
                    # (или их долях).
                    #
                    # Если базовая блокировка — RLock, она не снимается с помощью
                    # метода release(), поскольку это может фактически не разблокировать блокировку, когда она
                    # была получена несколько раз рекурсивно. Вместо этого используется внутренний интерфейс
                    # класса RLock, который действительно разблокирует ее, даже если она была
                    # получена рекурсивно несколько раз. Другой внутренний интерфейс затем используется для
                    # восстановления уровня рекурсии при повторном получении блокировки.
                    self.condition.wait()


# Пример результата выполнения программы:

bk = Bank()

# Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')

# Вывод на консоль (может отличаться значениями, логика должна быть та же):
# Пополнение: 241. Баланс: 241
# Запрос на 174
# Снятие: 174. Баланс: 67
# Пополнение: 226. Баланс: 293
# Запрос на 421
# Запрос отклонён, недостаточно средств
# Пополнение: 133. Баланс: 426
# Запрос на 422
# Снятие: 422. Баланс: 4
# Пополнение: 150. Баланс: 154
# Запрос на 207
# Запрос отклонён, недостаточно средств
# ....
# Запрос на 431
# Снятие: 431. Баланс: 276
# Запрос на 288
# Запрос отклонён, недостаточно средств
# Итоговый баланс: 276
