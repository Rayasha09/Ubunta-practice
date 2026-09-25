import time
import statistics
import urllib.request
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.gnu.org",
    "https://www.kernel.org",
] * 4

REPEATS = 3
WORKERS = 4


def download(url):
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "OS-Practice/1.0"}
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            return len(response.read())
    except Exception as error:
        return f"Ошибка: {error}"


def sequential():
    return [download(url) for url in URLS]


def threaded():
    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        return list(executor.map(download, URLS))


def multiprocess():
    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        return list(executor.map(download, URLS))


def benchmark(name, function):
    times = []
    for _ in range(REPEATS):
        start = time.perf_counter()
        results = function()
        times.append(time.perf_counter() - start)

    print(f"{name}:")
    print("  Время: " + ", ".join(f"{t:.2f} с" for t in times))
    print(f"  Медиана: {statistics.median(times):.2f} с")
    print(f"  Успешных загрузок: {sum(isinstance(x, int) for x in results)}/{len(URLS)}")


def main():
    print(f"URL: {len(URLS)}, потоков/процессов: {WORKERS}, повторов: {REPEATS}\n")
    benchmark("Последовательно", sequential)
    benchmark("ThreadPoolExecutor", threaded)
    benchmark("ProcessPoolExecutor", multiprocess)


if __name__ == "__main__":
    main()
