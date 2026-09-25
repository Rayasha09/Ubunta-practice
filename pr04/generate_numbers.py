#!/usr/bin/env python3
import random

COUNT = 10_000_000

with open("numbers.txt", "w") as f:
    for _ in range(COUNT):
        f.write(f"{random.randint(1, 100)}\n")

print(f"Создан numbers.txt: {COUNT:,} чисел")
