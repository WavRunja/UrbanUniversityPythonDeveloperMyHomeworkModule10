# module_10_3.py

import threading


# Реализуйте программу, которая имитирует доступ к общему ресурсу с использованием механизма блокировки потоков.

# Класс BankAccount должен отражать банковский счет с балансом и методами для пополнения и снятия денег.
# Необходимо использовать механизм блокировки, чтобы избежать проблемы гонок (race conditions)
# при модификации общего ресурса.
class BankAccount:
    def __init__(self, initial_balance=1000):
        # Баланс
        self.balance = initial_balance
        # Используйте класс Lock из модуля threading для блокировки доступа к общему ресурсу.
        self.lock = threading.Lock()

    # Метод для пополнения
    def deposit(self, amount):
        # Используйте with (lock object): в начале каждого метода, чтобы использовать блокировку
        with self.lock:
            # Пополняем баланс на сумму amount
            new_balance = self.balance + amount
            # Вывод: Внесенная сумма amount, новый баланс - new_balance.
            # print(f"Внесенная сумма {amount}, новый баланс - {new_balance}")
            print(f"Deposited {amount}, new balance is {new_balance}")
            # Присваиваем балансу новое значение.
            self.balance = new_balance

    # Метод для снятия денег
    def withdraw(self, amount):
        # Используйте with (lock object): в начале каждого метода, чтобы использовать блокировку
        with self.lock:
            # Если баланс больше снимаемой суммы
            if self.balance >= amount:
                # Уменьшаем баланс на сумму amount
                new_balance = self.balance - amount
                # print(f"Снятая сумма {amount}, новый баланс {new_balance}")
                print(f"Withdrew {amount}, new balance is {new_balance}")
                # Присваиваем балансу новое значение.
                self.balance = new_balance
            # Если снимаемая сумма превышает баланс
            else:
                # print(f"Не удалось вывести сумму {amount}, недостаточно средств. Текущий баланс — {self.balance}")
                print(f"Failed to withdraw {amount}, insufficient funds. Current balance is {self.balance}")


# Пример работы:
def deposit_task(account, amount):
    for _ in range(5):
        account.deposit(amount)


def withdraw_task(account, amount):
    for _ in range(5):
        account.withdraw(amount)


# Создаем экземпляр BankAccount
account = BankAccount()

# Создаем потоки для пополнения и снятия средств
deposit_thread = threading.Thread(target=deposit_task, args=(account, 100))
withdraw_thread = threading.Thread(target=withdraw_task, args=(account, 150))

# Запускаем потоки
deposit_thread.start()
withdraw_thread.start()

# Ожидаем завершения потоков
deposit_thread.join()
withdraw_thread.join()

# Вывод в консоль:
# Deposited 100, new balance is 1100
# Deposited 100, new balance is 1200
# Deposited 100, new balance is 1300
# Deposited 100, new balance is 1400
# Deposited 100, new balance is 1500
# Withdrew 150, new balance is 1350
# Withdrew 150, new balance is 1200
# Withdrew 150, new balance is 1050
# Withdrew 150, new balance is 900
# Withdrew 150, new balance is 750
