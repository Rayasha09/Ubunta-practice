#!/usr/bin/env python3
import os
import time


def get_rss_kb():
    with open("/proc/self/status", "r") as f:
        for line in f:
            if line.startswith("VmRSS:"):
                return int(line.split()[1])
    return 0


def main():
    data = bytearray(50 * 1024 * 1024)
    for i in range(0, len(data), 4096):
        data[i] = 1

    print(f"Родитель PID={os.getpid()}, RSS={get_rss_kb()} kB", flush=True)

    pid = os.fork()

    if pid == 0:
        print(f"Ребёнок до изменения: RSS={get_rss_kb()} kB", flush=True)

        for i in range(0, len(data), 4096):
            data[i] = 2

        print(f"Ребёнок после изменения: RSS={get_rss_kb()} kB", flush=True)
        os._exit(0)

    os.waitpid(pid, 0)
    print("Родитель дождался завершения ребёнка.", flush=True)


if __name__ == "__main__":
    main()
