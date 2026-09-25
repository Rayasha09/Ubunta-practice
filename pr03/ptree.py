import os

def read_process(pid):
    try:
        with open(f"/proc/{pid}/status", "r") as f:
            status = f.readlines()

        data = {}
        for line in status:
            if line.startswith(("Name:", "State:", "PPid:", "Uid:", "VmRSS:")):
                key, value = line.split(":", 1)
                data[key] = value.strip()

        uid = int(data["Uid"].split()[0])
        if uid != os.getuid():
            return None

        return {
            "pid": pid,
            "ppid": int(data.get("PPid", "0")),
            "name": data.get("Name", "?"),
            "state": data.get("State", "?"),
            "rss": data.get("VmRSS", "0 kB"),
        }
    except (OSError, ValueError, KeyError):
        return None


def main():
    processes = {}

    for entry in os.listdir("/proc"):
        if entry.isdigit():
            process = read_process(int(entry))
            if process:
                processes[process["pid"]] = process

    children = {}
    for process in processes.values():
        children.setdefault(process["ppid"], []).append(process)

    for group in children.values():
        group.sort(key=lambda p: p["pid"])

    def show(pid, indent=0, visited=None):
        if visited is None:
            visited = set()
        if pid in visited or pid not in processes:
            return

        visited.add(pid)
        p = processes[pid]
        print(
            "  " * indent
            + f'PID={p["pid"]} State={p["state"]} '
            + f'RSS={p["rss"]} Name={p["name"]}'
        )

        for child in children.get(pid, []):
            show(child["pid"], indent + 1, visited)

    roots = [
        p for p in processes.values()
        if p["ppid"] not in processes
    ]

    for root in sorted(roots, key=lambda p: p["pid"]):
        show(root["pid"])


if __name__ == "__main__":
    main()
