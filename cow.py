#!/usr/bin/env python3

import os
import time


def get_rss_kb():
    with open("/proc/self/status", "r") as f:
        for line in f:
            if line.startswith("VmRSS:"):
                return int(line.split()[1])

    return 0


# Большой список.
# 10 миллионов элементов занимают заметный объём памяти.
data = [0] * 10_000_000

print(
    f"Родитель PID={os.getpid()}, "
    f"RSS до fork: {get_rss_kb()} KB",
    flush=True
)

pid = os.fork()

if pid == 0:
    print(
        f"Ребёнок PID={os.getpid()}, "
        f"RSS сразу после fork: {get_rss_kb()} KB",
        flush=True
    )

    print("Изменяем большой список...", flush=True)

    # Меняем элементы по всей длине списка.
    # Это заставляет страницы памяти становиться приватными.
    for i in range(0, len(data), 512):
        data[i] = 1

    print(
        f"Ребёнок PID={os.getpid()}, "
        f"RSS после изменения списка: {get_rss_kb()} KB",
        flush=True
    )

    time.sleep(3)

    os._exit(0)

else:
    os.waitpid(pid, 0)

    print(
        f"Родитель PID={os.getpid()}, "
        f"RSS после завершения ребёнка: {get_rss_kb()} KB",
        flush=True
    )
