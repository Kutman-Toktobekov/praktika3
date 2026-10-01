#!/usr/bin/env python3

import os
import sys
import time


def main():
    if len(sys.argv) < 3:
        print("Использование:")
        print("python3 runner.py N команда [аргументы...]")
        print()
        print("Пример:")
        print("python3 runner.py 3 sleep 1")
        sys.exit(1)

    n = int(sys.argv[1])
    command = sys.argv[2:]

    children = []

    for i in range(n):
        start_time = time.monotonic()

        pid = os.fork()

        if pid == 0:
            # Дочерний процесс
            try:
                os.execvp(command[0], command)
            except FileNotFoundError:
                print(f"Команда не найдена: {command[0]}", file=sys.stderr)
                os._exit(127)
            except Exception as e:
                print(f"Ошибка exec: {e}", file=sys.stderr)
                os._exit(126)

        else:
            # Родитель
            children.append((pid, start_time))
            print(f"Создан процесс PID={pid}")

    print()
    print("Ожидание завершения процессов...")
    print()

    for pid, start_time in children:
        finished_pid, status = os.waitpid(pid, 0)

        elapsed = time.monotonic() - start_time

        if os.WIFEXITED(status):
            return_code = os.WEXITSTATUS(status)
            print(
                f"PID={finished_pid}: "
                f"код возврата={return_code}, "
                f"время={elapsed:.3f} сек"
            )

        elif os.WIFSIGNALED(status):
            signal_number = os.WTERMSIG(status)
            print(
                f"PID={finished_pid}: "
                f"завершён сигналом={signal_number}, "
                f"время={elapsed:.3f} сек"
            )


if __name__ == "__main__":
    main()
