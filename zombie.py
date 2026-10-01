#!/usr/bin/env python3

import os
import time


pid = os.fork()

if pid == 0:
    print(f"Ребёнок завершился. PID={os.getpid()}", flush=True)
    os._exit(0)

else:
    print(f"Родитель PID={os.getpid()}", flush=True)
    print(f"Ребёнок PID={pid}", flush=True)
    print("Родитель НЕ вызывает wait().", flush=True)
    print("Зомби будет существовать 20 секунд.", flush=True)

    time.sleep(20)

    os.waitpid(pid, 0)

    print("Родитель забрал статус ребёнка.", flush=True)
