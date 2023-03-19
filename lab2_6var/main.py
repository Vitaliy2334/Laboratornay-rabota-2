import os
import string
import hashlib
import re

def task1():
    print("#TASK #1")
    filename = "text.txt"
    with open(filename, 'r') as file:
        # словарь для хранения частоты встречаемых символов
        freq = {}
        # читаем файл построчно
        for line in file:
            # переводим все символы в нижний регистр
            line = line.lower()
            # удаляем символы пунктуации и пробелы
            line = line.translate(line.maketrans("", "", string.punctuation + " "))
            # обрабатываем каждую букву в строке
            for letter in line:
                if letter.isalpha():
                    # увеличиваем частосту встречаемости буквы в словаре
                    if letter in freq:
                        freq[letter] += 1
                    else:
                        freq[letter] = 1

    # Сортируем словарь по значению в порядке убывания
    sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    # вывод результата
    for letter, count in sorted_freq:
        print(letter, count)


# для этого задания необходимо заранее создать какую-либо папку и файлы дубликаты для корректной демонстрации работы.
def task2():
    print("TASK #2")

    files = {}

    def find_dups(dir):
        for dirpath, dirname, filenames in os.walk(dir):
            for filename in filenames:
                # получаем полный путь к файлу
                filepath = os.path.join(dirpath, filename)
                # Вычисляем MD5-хеш файла
                with open(filepath, 'rb') as f:
                    filehash = hashlib.md5(f.read()).hexdigest()
                # Добавляем файл в словарь
                if filehash in files:
                    files[filehash].append(filepath)
                else:
                    files[filehash] = [filepath]
        # Вовзрааем список групп файлов-дубликатов
        return [group for group in files.values() if len(group) > 1]

    # Вызываем локальную функцию
    duplicates = find_dups('task2')

    # Выводим список групп файлов-дубликатов
    for group in duplicates:
        print("Группа файлов дубликатов: ")
        for filename in group:
            print(f"\t{filename}")


def task3():
    print("TASK #3")
    dir_path = 'task3/songs'
    song_list_file = 'task3/songs_list.txt'

    with open(song_list_file, 'r') as f:
        song_list = f.readlines()

    for song in song_list:
        song_parts = song.strip().split('. ')
        song_num = song_parts[0]
        song_name = song_parts[1].split(' [')[0]

        for filename in os.listdir(dir_path):
            if song_name in filename:
                new_name = song_num + '. ' + song_name + os.path.splitext(filename)[1]
                os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_name))
                break


def task4():

    # Ввод имени файла
    filename = input("Введите имя файла: ")

    # Чтение файла
    with open(filename, "r") as file:
        content = file.read()

    # Поиск строк вида "x: type [N]"
    pattern = re.compile(r"(\w+): (int|short|byte) \[(\d+)\]")
    matches = pattern.finditer(content)

    # Вывод результатов поиска
    for match in matches:
        print(
            f"Строка ", content.count('\n', 0, match.start()) + 1,
            f", позиция {match.start()}: найдено '{match.group(0)}'")


def task5():

    text = input("Введите текст: ")
    pattern = r'\b[A-Z][a-z]*\d{2,4}\b'
    # \b - граница слова,
    # [A-Z] - любая заглавная буква латинского алфавита
    # [a-z]* - Любое кол-во строчных букв латинского алфавита
    # \d{2,4} - 2 или 4 цифры
    result = re.findall(pattern, text)

    print(result)

    # Пример вводимого текста: John21 is a Service2002 manager at XYZ Inc. Petr93 is a consultant.


def main():
    task1()
    task2()
    task3()
    task4()
    task5()


if __name__ == '__main__':
    main()
