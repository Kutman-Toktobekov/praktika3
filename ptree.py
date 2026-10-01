#!/usr/bin/env python3

import os


def read_process(pid):
    """Читает информацию о процессе из /proc/PID."""
    proc_dir = f"/proc/{pid}"

    try:
        stat = {}

        # Читаем /proc/PID/status
        with open(f"{proc_dir}/status", "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.split(":", 1)
                    stat[key.strip()] = value.strip()

        uid = int(stat["Uid"].split()[0])
        ppid = int(stat["PPid"])
        state = stat["State"].split()[0]
        rss = stat.get("VmRSS", "0 kB").split()[0]

        return {
            "pid": pid,
            "ppid": ppid,
            "uid": uid,
            "state": state,
            "rss": int(rss),
        }

    except (FileNotFoundError, ProcessLookupError, PermissionError, KeyError, ValueError):
        return None


def get_processes():
    """Получает процессы текущего пользователя."""
    current_uid = os.getuid()
    processes = {}

    for name in os.listdir("/proc"):
        if not name.isdigit():
            continue

        pid = int(name)
        info = read_process(pid)

        if info is None:
            continue

        if info["uid"] == current_uid:
            processes[pid] = info

    return processes


def build_tree(processes):
    """Создаёт структуру parent PID -> список дочерних PID."""
    children = {}

    for pid, info in processes.items():
        ppid = info["ppid"]
        children.setdefault(ppid, []).append(pid)

    for ppid in children:
        children[ppid].sort()

    return children


def print_tree(pid, processes, children, level=0):
    """Рекурсивно печатает дерево процессов."""
    if pid not in processes:
        return

    info = processes[pid]

    indent = "  " * level

    print(
        f"{indent}PID={info['pid']} "
        f"STATE={info['state']} "
        f"RSS={info['rss']} KB"
    )

    for child_pid in children.get(pid, []):
        print_tree(child_pid, processes, children, level + 1)


def main():
    processes = get_processes()
    children = build_tree(processes)

    # Корневые процессы:
    # их родитель отсутствует среди процессов текущего пользователя
    roots = []

    for pid, info in processes.items():
        if info["ppid"] not in processes:
            roots.append(pid)

    roots.sort()

    print("Дерево процессов текущего пользователя:")
    print()

    for root in roots:
        print_tree(root, processes, children)


if __name__ == "__main__":
    main()#!/usr/bin/env python3

import os


def read_process(pid):
    """Читает информацию о процессе из /proc/PID."""
    proc_dir = f"/proc/{pid}"

    try:
        stat = {}

        # Читаем /proc/PID/status
        with open(f"{proc_dir}/status", "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.split(":", 1)
                    stat[key.strip()] = value.strip()

        uid = int(stat["Uid"].split()[0])
        ppid = int(stat["PPid"])
        state = stat["State"].split()[0]
        rss = stat.get("VmRSS", "0 kB").split()[0]

        return {
            "pid": pid,
            "ppid": ppid,
            "uid": uid,
            "state": state,
            "rss": int(rss),
        }

    except (FileNotFoundError, ProcessLookupError, PermissionError, KeyError, ValueError):
        return None


def get_processes():
    """Получает процессы текущего пользователя."""
    current_uid = os.getuid()
    processes = {}

    for name in os.listdir("/proc"):
        if not name.isdigit():
            continue

        pid = int(name)
        info = read_process(pid)

        if info is None:
            continue

        if info["uid"] == current_uid:
            processes[pid] = info

    return processes


def build_tree(processes):
    """Создаёт структуру parent PID -> список дочерних PID."""
    children = {}

    for pid, info in processes.items():
        ppid = info["ppid"]
        children.setdefault(ppid, []).append(pid)

    for ppid in children:
        children[ppid].sort()

    return children


def print_tree(pid, processes, children, level=0):
    """Рекурсивно печатает дерево процессов."""
    if pid not in processes:
        return

    info = processes[pid]

    indent = "  " * level

    print(
        f"{indent}PID={info['pid']} "
        f"STATE={info['state']} "
        f"RSS={info['rss']} KB"
    )

    for child_pid in children.get(pid, []):
        print_tree(child_pid, processes, children, level + 1)


def main():
    processes = get_processes()
    children = build_tree(processes)

    # Корневые процессы:
    # их родитель отсутствует среди процессов текущего пользователя
    roots = []

    for pid, info in processes.items():
        if info["ppid"] not in processes:
            roots.append(pid)

    roots.sort()

    print("Дерево процессов текущего пользователя:")
    print()

    for root in roots:
        print_tree(root, processes, children)


if __name__ == "__main__":
    main()
