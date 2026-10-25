"""main.py - MiniOS shell.

Run with:  python main.py
This file owns the command loop and dispatches each command to the
module that handles it (users, filesystem, processes, memory).
"""

import os
import shlex
import sys
from datetime import datetime

from filesystem import FileSystem
from memory import MemoryManager
from processes import KNOWN_PROGRAMS, ProcessManager
from users import UserManager

OS_NAME = "Marquez and Friends MiniOS"
VERSION = "1.0"

BANNER = f"""========================================
          {OS_NAME.upper()} v{VERSION}
========================================

Welcome to Marquez and Friends MiniOS!
"""

HELP_TEXT = """Available Commands:

General
  help                  Show this list
  clear                 Clear the screen
  date                  Show the current date
  time                  Show the current time
  whoami                Show the logged-in user
  systeminfo            Show system information
  version               Show the MiniOS version
  echo <text>           Print text
  history               Show commands used this session
  exit                  Shut down MiniOS

Users
  users                 List accounts
  logout                Log out and return to login screen

File Management
  dir                   List files and folders
  mkdir <name>          Create a directory
  create <name>         Create an empty file
  read <name>           Show a file's contents
  write <name> <text>   Replace a file's contents
  delete <name>         Delete a file or empty directory
  rename <old> <new>    Rename a file or directory
  cd <path>             Change directory (cd .. goes up)

Process Management
  process               List processes
  run <program>         Start a simulated process
  kill <pid>            Terminate a process
  suspend <pid>         Pause a process
  resume <pid>          Continue a paused process

Memory Management
  memory                Show memory status
  allocate <MB>         Allocate memory
  free <MB>             Release memory
"""


class MiniOS:
    def __init__(self):
        self.users = UserManager()
        self.memory = MemoryManager()
        self.fs = FileSystem()
        self.procs = ProcessManager(self.memory)
        self.history = []
        self.running = True

        self.commands = {
            "help": self.cmd_help,
            "clear": self.cmd_clear,
            "cls": self.cmd_clear,
            "date": self.cmd_date,
            "time": self.cmd_time,
            "whoami": self.cmd_whoami,
            "systeminfo": self.cmd_systeminfo,
            "version": self.cmd_version,
            "echo": self.cmd_echo,
            "history": self.cmd_history,
            "exit": self.cmd_exit,
            "shutdown": self.cmd_exit,
            "users": self.cmd_users,
            "logout": self.cmd_logout,
            "dir": self.cmd_dir,
            "ls": self.cmd_dir,
            "mkdir": self.cmd_mkdir,
            "create": self.cmd_create,
            "read": self.cmd_read,
            "write": self.cmd_write,
            "delete": self.cmd_delete,
            "rename": self.cmd_rename,
            "cd": self.cmd_cd,
            "process": self.cmd_process,
            "run": self.cmd_run,
            "kill": self.cmd_kill,
            "suspend": self.cmd_suspend,
            "resume": self.cmd_resume,
            "memory": self.cmd_memory,
            "allocate": self.cmd_allocate,
            "free": self.cmd_free,
        }

    # ---- helpers -------------------------------------------------------
    @staticmethod
    def _need(args, count, usage):
        if len(args) < count:
            print(f"Error: Missing argument.\nUsage: {usage}")
            return False
        return True

    @staticmethod
    def _to_int(text, label):
        try:
            return int(text)
        except ValueError:
            print(f"Error: {label} must be a whole number.")
            return None

    # ---- general -------------------------------------------------------
    def cmd_help(self, args):
        print(HELP_TEXT)

    def cmd_clear(self, args):
        os.system("cls" if os.name == "nt" else "clear")

    def cmd_date(self, args):
        print(datetime.now().strftime("Current Date: %A, %B %d, %Y"))

    def cmd_time(self, args):
        print(datetime.now().strftime("Current Time: %I:%M:%S %p"))

    def cmd_whoami(self, args):
        print(f"Current User: {self.users.current_user}")

    def cmd_version(self, args):
        print(f"{OS_NAME} version {VERSION}")

    def cmd_echo(self, args):
        print(" ".join(args))

    def cmd_history(self, args):
        if not self.history:
            print("No commands yet.")
        for i, line in enumerate(self.history, 1):
            print(f"{i:>3}  {line}")

    def cmd_systeminfo(self, args):
        print("=" * 40)
        print("          SYSTEM INFORMATION")
        print("=" * 40)
        print()
        print(f"OS Name: {OS_NAME}")
        print(f"Version: {VERSION}")
        print("Architecture: 64-bit")
        print("CPU: Virtual CPU")
        print(f"Memory: {self.memory.total} MB")
        print(f"User: {self.users.current_user} ({self.users.role()})")
        print(f"Running Processes: {len(self.procs.table)}")
        print()
        print("=" * 40)

    def cmd_exit(self, args):
        self.procs.kill_all()
        print("\nShutting down MiniOS...\n")
        print("Goodbye!")
        self.running = False

    # ---- users ---------------------------------------------------------
    def cmd_users(self, args):
        print("USERNAME     ROLE")
        for name, role in self.users.list_users():
            marker = "  (you)" if name == self.users.current_user else ""
            print(f"{name:<12} {role}{marker}")

    def cmd_logout(self, args):
        self.procs.kill_all()
        self.users.logout()
        print("Logged out.\n")
        self.login_loop()

    # ---- files ---------------------------------------------------------
    def cmd_dir(self, args):
        print(f"Directory of {self.fs.path()}\n")
        items = self.fs.listing()
        if not items:
            print("(empty)")
            return
        for name, is_dir, size in items:
            kind = "<DIR>" if is_dir else f"{size} B"
            print(f"{kind:>8}   {name}")

    def cmd_mkdir(self, args):
        if self._need(args, 1, "mkdir <name>"):
            print(self.fs.mkdir(args[0]))

    def cmd_create(self, args):
        if self._need(args, 1, "create <name>"):
            print(self.fs.create(args[0]))

    def cmd_read(self, args):
        if self._need(args, 1, "read <name>"):
            print(self.fs.read(args[0]))

    def cmd_write(self, args):
        if self._need(args, 2, "write <name> <text>"):
            print(self.fs.write(args[0], " ".join(args[1:])))

    def cmd_delete(self, args):
        if self._need(args, 1, "delete <name>"):
            print(self.fs.delete(args[0]))

    def cmd_rename(self, args):
        if self._need(args, 2, "rename <old> <new>"):
            print(self.fs.rename(args[0], args[1]))

    def cmd_cd(self, args):
        if self._need(args, 1, "cd <path>"):
            msg = self.fs.cd(args[0])
            if msg:
                print(msg)

    # ---- processes -----------------------------------------------------
    def cmd_process(self, args):
        procs = self.procs.listing()
        if not procs:
            print("No running processes.")
            return
        print(f"{'PID':<6} {'NAME':<14} {'STATUS':<10} MEM")
        for p in procs:
            print(f"{p.pid:<6} {p.name:<14} {p.status:<10} {p.memory_mb} MB")

    def cmd_run(self, args):
        if not self._need(args, 1, "run <program>"):
            return
        name = args[0].lower()
        if name not in KNOWN_PROGRAMS:
            print(f"Error: Program not found.\nAvailable programs: {', '.join(KNOWN_PROGRAMS)}")
            return
        proc, err = self.procs.run(name)
        if err:
            print(err)
            return
        print("\nProcess started.\n")
        print(f"PID: {proc.pid}")
        print(f"Name: {proc.name}")
        print(f"Status: {proc.status}")

    def cmd_kill(self, args):
        if not self._need(args, 1, "kill <pid>"):
            return
        pid = self._to_int(args[0], "PID")
        if pid is not None:
            print(self.procs.kill(pid))

    def cmd_suspend(self, args):
        if not self._need(args, 1, "suspend <pid>"):
            return
        pid = self._to_int(args[0], "PID")
        if pid is not None:
            print(self.procs.suspend(pid))

    def cmd_resume(self, args):
        if not self._need(args, 1, "resume <pid>"):
            return
        pid = self._to_int(args[0], "PID")
        if pid is not None:
            print(self.procs.resume(pid))

    # ---- memory --------------------------------------------------------
    def cmd_memory(self, args):
        print(self.memory.status())

    def cmd_allocate(self, args):
        if not self._need(args, 1, "allocate <MB>"):
            return
        amount = self._to_int(args[0], "Amount")
        if amount is not None:
            print(self.memory.allocate(amount))

    def cmd_free(self, args):
        if not self._need(args, 1, "free <MB>"):
            return
        amount = self._to_int(args[0], "Amount")
        if amount is not None:
            print(self.memory.free(amount))

    # ---- main loop -----------------------------------------------------
    def login_loop(self):
        while not self.users.login_prompt():
            print("Too many failed attempts. Try again.\n")

    def execute(self, line):
        try:
            parts = shlex.split(line)
        except ValueError:
            print("Error: Unbalanced quotes in command.")
            return
        if not parts:
            return
        name, args = parts[0].lower(), parts[1:]
        handler = self.commands.get(name)
        if handler is None:
            print("Unknown command.\n\nType 'help' to see the available commands.")
            return
        try:
            handler(args)
        except Exception as exc:  # last line of defense so the shell never crashes
            print(f"Error: Something went wrong ({exc}).")

    def start(self):
        print(BANNER)
        try:
            self.login_loop()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
        while self.running:
            try:
                line = input(f"\nMiniOS {self.fs.path()}> ")
            except (EOFError, KeyboardInterrupt):
                print()
                self.cmd_exit([])
                break
            if line.strip():
                self.history.append(line.strip())
            self.execute(line)


if __name__ == "__main__":
    MiniOS().start()
    sys.exit(0)
