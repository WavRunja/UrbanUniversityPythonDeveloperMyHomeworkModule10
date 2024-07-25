# module_10_1.py

# Домашнее задание по теме "Создание потоков".

# Задача "Потоковая запись в файлы".

# Алгоритм работы кода:
# Импорты необходимых модулей и функций
# Объявление функции write_words
# Взятие текущего времени
# Запуск функций с аргументами из задачи
# Взятие текущего времени
# Вывод разницы начала и конца работы функций
# Взятие текущего времени
# Создание и запуск потоков с аргументами из задачи
# Взятие текущего времени
# Вывод разницы начала и конца работы потоков

from time import sleep
from datetime import datetime
from threading import Thread


# Необходимо создать функцию wite_words(word_count, file_name),
# где word_count - количество записываемых слов,
# file_name - название файла, куда будут записываться слова.
def write_words(word_count, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        for i in range(1, word_count + 1):
            # Функция должна вести запись слов "Какое-то слово № <номер слова по порядку>"
            # в соответствующий файл с прерыванием после записи каждого на 0.1 секунду.
            f.write(f"Какое-то слово № {i}\n")
            # Сделать паузу можно при помощи функции sleep из модуля time,
            # предварительно импортировав её: from time import sleep.
            sleep(0.1)
    # В конце работы функции вывести строку "Завершилась запись в файл <название файла>".
    print(f"Завершилась запись в файл {file_name}")


# Время выполнения без потоков
time_start = datetime.now()

# После создания файла вызовите 4 раза функцию wite_words, передав в неё следующие значения:
# 10, example1.txt
# 30, example2.txt
# 200, example3.txt
# 100, example4.txt
write_words(10, 'example1.txt')
write_words(30, 'example2.txt')
write_words(200, 'example3.txt')
write_words(100, 'example4.txt')

time_end = datetime.now()
time_res = time_end - time_start
print(f"Работа потоков {time_res}")

# Время выполнения с потоками
time_start = datetime.now()

threads = [
    # После вызовов функций создайте 4 потока для вызова этой функции со следующими аргументами для функции:
    # 10, example5.txt
    # 30, example6.txt
    # 200, example7.txt
    # 100, example8.txt
    Thread(target=write_words, args=(10, 'example5.txt')),
    Thread(target=write_words, args=(30, 'example6.txt')),
    Thread(target=write_words, args=(200, 'example7.txt')),
    Thread(target=write_words, args=(100, 'example8.txt'))
]

# Запустите эти потоки методом start не забыв, сделать остановку основного потока при помощи join.
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

# Также измерьте время затраченное на выполнение функций и потоков.
# Как это сделать рассказано в лекции к домашнему заданию.
time_end = datetime.now()
time_res = time_end - time_start
print(f"Работа потоков {time_res}")

# Вывод на консоль:
# Завершилась запись в файл example1.txt
# Завершилась запись в файл example2.txt
# Завершилась запись в файл example3.txt
# Завершилась запись в файл example4.txt
# Работа потоков 0:00:34.003411 # Может быть другое время.
# Завершилась запись в файл example5.txt
# Завершилась запись в файл example6.txt
# Завершилась запись в файл example8.txt
# Завершилась запись в файл example7.txt
# Работа потоков 0:00:20.071575 # Может быть другое время.
