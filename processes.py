"""processes.py - Simulated process management for MiniOS.

Processes are just records in a table. Each one gets a PID and a status.
Nothing here starts or stops a real Windows process.
"""

from datetime import datetime

KNOWN_PROGRAMS = ["calculator", "editor", "notepad", "browser", "terminal", "clock"]


class Process:
    def __init__(self, pid, name, memory_mb=0):
        self.pid = pid
        self.name = name
        self.status = "RUNNING"
        self.memory_mb = memory_mb
        self.started = datetime.now()


class ProcessManager:
    def __init__(self, memory_manager=None):
        self.table = {}
        self.next_pid = 1
        self.memory = memory_manager

    def run(self, name, mem_cost=16):
        """Start a process. Each process reserves a small slice of simulated memory."""
        name = name.lower()
        if self.memory is not None:
            ok = self.memory.reserve_for_process(mem_cost)
            if not ok:
                return None, "Error: Not enough free memory to start this process."
        proc = Process(self.next_pid, name, mem_cost)
        self.table[proc.pid] = proc
        self.next_pid += 1
        return proc, ""

    def kill(self, pid):
        proc = self.table.get(pid)
        if proc is None:
            return "Error: Process does not exist."
        if self.memory is not None:
            self.memory.release_from_process(proc.memory_mb)
        del self.table[pid]
        return f"Process {pid} terminated."

    def suspend(self, pid):
        proc = self.table.get(pid)
        if proc is None:
            return "Error: Process does not exist."
        if proc.status == "SUSPENDED":
            return "Error: Process is already suspended."
        proc.status = "SUSPENDED"
        return f"Process {pid} suspended."

    def resume(self, pid):
        proc = self.table.get(pid)
        if proc is None:
            return "Error: Process does not exist."
        if proc.status == "RUNNING":
            return "Error: Process is already running."
        proc.status = "RUNNING"
        return f"Process {pid} resumed."

    def listing(self):
        return sorted(self.table.values(), key=lambda p: p.pid)

    def kill_all(self):
        for pid in list(self.table):
            self.kill(pid)
