#!/usr/bin/env python3

import os
import time


pid = os.fork()

if pid == 0:
    # Ребёнок
    print(f"Ребёнок: PID={os.getpid()}", flush=True)
    print(f"Ребёнок: первоначальный PPID={os.getppid()}", flush=True)

    time.sleep(5)

    print(f"Ребёнок: новый PPID={os.getppid()}", flush=True)

    time.sleep(5)

else:
    # Родитель
    print(f"Родитель: PID={os.getpid()}", flush=True)
    print(f"Родитель: ребёнок PID={pid}", flush=True)

    print("Родитель сейчас завершится.", flush=True)

    os._exit(0)
