import multiprocessing
import threading
import time
import statistics
import os

FILE = "numbers.txt"
REPEATS = 3
WORKERS = 4


def sum_single(numbers):
    return sum(numbers)


def sum_threads(numbers):
    size = len(numbers) // WORKERS
    results = [0] * WORKERS

    def worker(i, start, end):
        results[i] = sum(numbers[start:end])

    threads = []
    for i in range(WORKERS):
        start = i * size
        end = len(numbers) if i == WORKERS - 1 else (i + 1) * size
        t = threading.Thread(target=worker, args=(i, start, end))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return sum(results)


def sum_processes(numbers):
    size = len(numbers) // WORKERS
    chunks = [
        numbers[i * size:len(numbers) if i == WORKERS - 1 else (i + 1) * size]
        for i in range(WORKERS)
    ]

    with multiprocessing.Pool(WORKERS) as pool:
        return sum(pool.map(sum, chunks))


def benchmark(func, numbers):
    times = []
    result = None

    for _ in range(REPEATS):
        start = time.perf_counter()
        result = func(numbers)
        times.append(time.perf_counter() - start)

    return result, times, statistics.median(times)


def main():
    if not os.path.exists(FILE):
        print("Файл numbers.txt не найден. Запусти python3 generate_numbers.py")
        return

    print(f"CPU по os.cpu_count(): {os.cpu_count()}")
    print(f"Повторов: {REPEATS}")
    print("Читаем данные...")
    with open(FILE) as f:
        numbers = [int(line) for line in f]

    print(f"Чисел: {len(numbers)}")
    expected = sum(numbers)
    print(f"Контрольная сумма: {expected}\n")

    for name, func in [
        ("Один поток", sum_single),
        ("4 потока", sum_threads),
        ("4 процесса", sum_processes),
    ]:
        result, times, median = benchmark(func, numbers)
        print(f"{name}: сумма={result}; совпадает={result == expected}")
        print("Время: " + ", ".join(f"{x:.3f} с" for x in times))
        print(f"Медиана: {median:.3f} с\n")


if __name__ == "__main__":
    main()
