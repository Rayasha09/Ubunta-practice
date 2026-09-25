import argparse
from collections import deque
from dataclasses import dataclass
import heapq


@dataclass
class Process:
    pid: str
    arrival: int
    burst: int
    priority: int


def load_processes(filename):
    processes = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pid, arrival, burst, priority = line.split()
            processes.append(Process(pid, int(arrival), int(burst), int(priority)))
    return processes


def simulate(processes, algorithm, quantum=3, aging=5):
    procs = sorted(processes, key=lambda p: (p.arrival, int(p.pid[1:])))
    remaining = {p.pid: p.burst for p in procs}
    first_start = {}
    completion = {}
    intervals = []
    time = 0
    current = None
    ready = deque()
    added = set()
    switches = 0
    last_pid = None

    def add_arrivals(t):
        for p in procs:
            if p.arrival <= t and p.pid not in added:
                ready.append(p)
                added.add(p.pid)

    if algorithm == "fcfs":
        for p in procs:
            time = max(time, p.arrival)
            start = time
            first_start.setdefault(p.pid, start)
            time += p.burst
            completion[p.pid] = time
            intervals.append((start, time, p.pid))
        return intervals, first_start, completion, switches

    if algorithm == "sjf":
        done = set()
        while len(done) < len(procs):
            available = [p for p in procs if p.pid not in done and p.arrival <= time]
            if not available:
                time = min(p.arrival for p in procs if p.pid not in done)
                continue
            p = min(available, key=lambda p: (p.burst, p.arrival, int(p.pid[1:])))
            first_start.setdefault(p.pid, time)
            start = time
            time += p.burst
            completion[p.pid] = time
            intervals.append((start, time, p.pid))
            done.add(p.pid)
        return intervals, first_start, completion, switches

    while len(completion) < len(procs):
        add_arrivals(time)
        ready = deque(p for p in ready if remaining[p.pid] > 0)

        available = [p for p in procs if p.arrival <= time and remaining[p.pid] > 0]
        if not available:
            time += 1
            continue

        if algorithm == "rr":
            if not ready:
                ready.extend(sorted(available, key=lambda p: (p.arrival, int(p.pid[1:]))))
            p = ready.popleft()
            run = min(quantum, remaining[p.pid])
        elif algorithm == "srtf":
            p = min(available, key=lambda p: (remaining[p.pid], p.arrival, int(p.pid[1:])))
            run = 1
        elif algorithm == "priority":
            waiting = {
                p.pid: max(0, time - p.arrival - (p.burst - remaining[p.pid]))
                for p in available
            }
            p = min(
                available,
                key=lambda p: (
                    max(0, p.priority - waiting[p.pid] // aging),
                    p.arrival,
                    int(p.pid[1:])
                )
            )
            run = 1
        else:
            raise ValueError("Неизвестный алгоритм")

        first_start.setdefault(p.pid, time)
        if last_pid is not None and last_pid != p.pid:
            switches += 1
        last_pid = p.pid
        start = time
        end = time + run

        if algorithm == "rr":
            for t in range(start + 1, end + 1):
                add_arrivals(t)
            time = end
            remaining[p.pid] -= run
            intervals.append((start, end, p.pid))
            if remaining[p.pid] == 0:
                completion[p.pid] = time
            else:
                ready.append(p)
        else:
            time += 1
            remaining[p.pid] -= 1
            if intervals and intervals[-1][2] == p.pid and intervals[-1][1] == start:
                intervals[-1] = (intervals[-1][0], time, p.pid)
            else:
                intervals.append((start, time, p.pid))
            if remaining[p.pid] == 0:
                completion[p.pid] = time

    return intervals, first_start, completion, switches


def metrics(processes, intervals, first_start, completion):
    n = len(processes)
    waiting = []
    turnaround = []
    response = []
    for p in processes:
        turnaround.append(completion[p.pid] - p.arrival)
        waiting.append(turnaround[-1] - p.burst)
        response.append(first_start[p.pid] - p.arrival)

    total_burst = sum(p.burst for p in processes)
    total_time = max(completion.values()) - min(p.arrival for p in processes)
    cpu_util = 100 * total_burst / total_time if total_time else 0
    return (
        sum(waiting) / n,
        sum(turnaround) / n,
        sum(response) / n,
        cpu_util,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", required=True,
                        choices=["fcfs", "sjf", "srtf", "priority", "rr"])
    parser.add_argument("--quantum", type=int, default=3)
    parser.add_argument("--aging", type=int, default=5)
    parser.add_argument("file")
    args = parser.parse_args()

    processes = load_processes(args.file)
    intervals, first, completion, switches = simulate(
        processes, args.algo, args.quantum, args.aging
    )
    avg_wait, avg_turn, avg_resp, cpu = metrics(
        processes, intervals, first, completion
    )

    print(f"Алгоритм: {args.algo}")
    if args.algo == "rr":
        print(f"Квант: {args.quantum}")
    print("Диаграмма Ганта:")
    print(" | ".join(f"{start}-{end}:{pid}" for start, end, pid in intervals))
    print(f"Среднее ожидание: {avg_wait:.2f}")
    print(f"Средний оборот: {avg_turn:.2f}")
    print(f"Средний отклик: {avg_resp:.2f}")
    print(f"Загрузка CPU: {cpu:.2f}%")
    print(f"Переключения: {switches}")


if __name__ == "__main__":
    main()
