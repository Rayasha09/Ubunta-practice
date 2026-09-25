import os
import sys

filename = sys.argv[1]

size = os.path.getsize(filename)

print(f"Размер файла: {size} байт")
