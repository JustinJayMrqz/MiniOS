"""memory.py - Simulated memory management for MiniOS.

We track two numbers: memory the user allocated by hand, and memory
reserved by running processes. Total memory is fixed at 1024 MB.
"""

TOTAL_MB = 1024
BASE_USED_MB = 256  # pretend the "kernel" already uses this much


class MemoryManager:
    def __init__(self, total=TOTAL_MB, base_used=BASE_USED_MB):
        self.total = total
        self.system_used = base_used
        self.user_allocated = 0
        self.process_used = 0

    @property
    def used(self):
        return self.system_used + self.user_allocated + self.process_used

    @property
    def free_mb(self):
        return self.total - self.used

    def status(self):
        return (
            "Memory Status\n"
            "------------------------\n"
            f"Total Memory: {self.total:>5} MB\n"
            f"Used Memory:  {self.used:>5} MB\n"
            f"Free Memory:  {self.free_mb:>5} MB"
        )

    def allocate(self, amount):
        if amount <= 0:
            return "Error: Amount must be greater than zero."
        if amount > self.free_mb:
            return f"Error: Not enough free memory. Only {self.free_mb} MB available."
        self.user_allocated += amount
        return f"{amount} MB allocated."

    def free(self, amount):
        if amount <= 0:
            return "Error: Amount must be greater than zero."
        if amount > self.user_allocated:
            return f"Error: You only have {self.user_allocated} MB allocated to free."
        self.user_allocated -= amount
        return f"{amount} MB released."

    # used by the process manager
    def reserve_for_process(self, amount):
        if amount > self.free_mb:
            return False
        self.process_used += amount
        return True

    def release_from_process(self, amount):
        self.process_used = max(0, self.process_used - amount)
