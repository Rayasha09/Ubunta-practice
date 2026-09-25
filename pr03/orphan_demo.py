#!/usr/bin/env python3
import os
import time

pid = os.fork()

if pid == 0:
    print(
        f"Ребёнок: PID={os.getpid()}, исходный PPID={os.getppid()}",
        flush=True,
    )
    time.sleep(2)
    print(
        f"После завершения родителя: PID={os.getpid()}, "
        f"новый PPID={os.getppid()}",
        flush=True,
    )
    time.sleep(3)
    os._exit(0)
else:
    print(
        f"Родитель PID={os.getpid()} завершается, ребёнок PID={pid}",
        flush=True,
    )
    os._exit(0)
