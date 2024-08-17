# Домашнее задание по теме "Многопроцессное программирование"

# Задача "Многопроцессное считывание"

import multiprocessing
from datetime import datetime


# Создайте функцию read_info(name), где name - название файла. Функция должна:
def read_info(name):
    # 1. Создавать локальный список all_data.
    all_data = []
    # 2. Открывать файл name для чтения.
    with open(name, 'r') as file:
        # 3. Считывать информацию построчно (readline),
        line = file.readline()
        # пока считанная строка не окажется пустой.
        while line:
            # 4. Во время считывания добавлять каждую строку в список all_data.
            all_data.append(line.strip())
            line = file.readline()


if __name__ == '__main__':
    # 1. Создайте список названий файлов в соответствии с названиями файлов архива.
    filenames = [f'file {number}.txt' for number in range(1, 5)]

    # 2. Вызовите функцию read_info для каждого файла по очереди (линейно)
    # и измерьте время выполнения и выведите его в консоль.
    start_time = datetime.now()
    for filename in filenames:
        read_info(filename)
    linear_duration = datetime.now() - start_time
    print(f"{linear_duration} (линейный)")

    # 3. Вызовите функцию read_info для каждого файла, используя многопроцессный подход:
    start_time = datetime.now()
    # контекстный менеджер with и объект Pool.
    with multiprocessing.Pool(processes=len(filenames)) as pool:
        # Для вызова функции используйте метод map, передав в него функцию read_info и список названий файлов.
        pool.map(read_info, filenames)
    # Измерьте время выполнения и выведите его в консоль.
    multiprocess_duration = datetime.now() - start_time
    print(f"{multiprocess_duration} (многопроцессный)")

    # Вывод на консоль, 2 запуска (результаты могут отличаться):
    # 0:00:03.046163 (линейный)
    # 0:00:01.092300 (многопроцессный)
