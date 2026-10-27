
import os
import sys

if len(sys.argv) != 2:
    print("Использование: python3 hello.py <путь_к_файлу>")
    sys.exit(1)

filename = sys.argv[1]

if not os.path.isfile(filename):
    print(f"Ошибка: файл не найден: {filename}")
    sys.exit(1)

size = os.path.getsize(filename)

print(f"Файл: {filename}")
print(f"Размер файла: {size} байт")
