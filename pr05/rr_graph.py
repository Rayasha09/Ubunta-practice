import subprocess
import re
import matplotlib.pyplot as plt

quanta = range(1, 11)
waiting = []
switches = []

for q in quanta:
    result = subprocess.run(
        ["python3", "sched.py", "--algo", "rr", "--quantum", str(q), "set2.txt"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    waiting.append(float(re.search(r"Среднее ожидание: ([\d.]+)", result).group(1)))
    switches.append(int(re.search(r"Переключения: (\d+)", result).group(1)))

print("Квант | Среднее ожидание | Переключения")
for q, w, s in zip(quanta, waiting, switches):
    print(f"{q:5} | {w:16.2f} | {s:12}")

plt.figure()
plt.plot(list(quanta), waiting, marker="o")
plt.xlabel("Квант RR")
plt.ylabel("Среднее ожидание")
plt.title("Квант и среднее ожидание")
plt.grid(True)
plt.savefig("rr_waiting.png", dpi=150)
plt.close()

plt.figure()
plt.plot(list(quanta), switches, marker="o")
plt.xlabel("Квант RR")
plt.ylabel("Число переключений")
plt.title("Квант и переключения")
plt.grid(True)
plt.savefig("rr_switches.png", dpi=150)
plt.close()

print("Графики сохранены: rr_waiting.png, rr_switches.png")
