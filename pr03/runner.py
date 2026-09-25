import os
import sys
import time


def main():
    if len(sys.argv) < 3:
        print("Использование: python3 runner.py N команда [аргументы...]")
        print("Пример: python3 runner.py 3 sleep 1")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
        if n < 1:
            raise ValueError
    except ValueError:
        print("Ошибка: N должно быть положительным числом")
        sys.exit(1)

    command = sys.argv[2:]
    children = {}

    for i in range(n):
        start = time.monotonic()

        try:
            pid = os.fork()
        except OSError as e:
            print(f"Не удалось создать процесс: {e}", file=sys.stderr)
            break

        if pid == 0:
            try:
                os.execvp(command[0], command)
            except OSError as e:
                print(f"Ошибка запуска команды: {e}", file=sys.stderr)
                os._exit(127)

        children[pid] = (i + 1, start)

    while children:
        try:
            pid, status = os.wait()
        except ChildProcessError:
            break

        number, start = children.pop(pid)
        elapsed = time.monotonic() - start

        if os.WIFEXITED(status):
            code = os.WEXITSTATUS(status)
        elif os.WIFSIGNALED(status):
            code = 128 + os.WTERMSIG(status)
        else:
            code = -1

        print(
            f"Ребёнок #{number}, PID={pid}: "
            f"код возврата={code}, время={elapsed:.3f} сек."
        )




if __name__  == "__main__":
    main()
