#!/usr/bin/env python3
import os
import time

pid = os.fork()

if pid == 0:
    print(f"Ребёнок завершился: PID={os.getpid()}", flush=True)
    os._exit(0)

print(f"Родитель: PID={os.getpid()}, ребёнок PID={pid}", flush=True)
print("Через 2 секунды проверь состояние ребёнка командой ps.", flush=True)

time.sleep(30)

os.waitpid(pid, 0)
print("Родитель забрал статус ребёнка. Зомби исчез.", flush=True)
