# MiniOS Alpha

A command-line operating system simulator written in Python for our Operating Systems final project. It runs in Windows Command Prompt and simulates users, files, processes and memory. It is not a real OS and never touches your actual files, processes or RAM.

## How to run

1. Install Python 3.8 or newer (tick "Add Python to PATH" during install).
2. Open Command Prompt and go to the project folder:
   ```
   cd path\to\MiniOS
   ```
3. Start it:
   ```
   python main.py
   ```

## Login accounts

| Username | Password   | Role           |
|----------|------------|----------------|
| admin    | admin123   | Administrator  |
| student  | student123 | Standard User  |

## Project structure

```
MiniOS/
├── main.py            Shell loop and command dispatcher
├── users.py           Login and accounts
├── filesystem.py      Virtual file system
├── processes.py       Simulated process table
├── memory.py          Simulated memory
├── requirements.txt
├── docs/              User manual and technical documentation
├── screenshots/       Screenshots for the report
└── individual-reports/
```

## Commands

**General:** help, clear, date, time, whoami, systeminfo, version, echo, history, exit
**Users:** users, logout
**Files:** dir, mkdir, create, read, write, delete, rename, cd
**Processes:** process, run, kill, suspend, resume
**Memory:** memory, allocate, free

Programs you can start with `run`: calculator, editor, notepad, browser, terminal, clock.

## Quick demo

```
MiniOS \> mkdir Documents
MiniOS \> cd Documents
MiniOS \Documents> create notes.txt
MiniOS \Documents> write notes.txt Hello from MiniOS
MiniOS \Documents> read notes.txt
MiniOS \Documents> run calculator
MiniOS \Documents> process
MiniOS \Documents> allocate 200
MiniOS \Documents> memory
MiniOS \Documents> systeminfo
MiniOS \Documents> exit
```

## How the simulation works

- **File system:** a tree of Python objects in memory. Files disappear when MiniOS exits.
- **Processes:** a dictionary of PID to process records. Each process reserves 16 MB of simulated memory, and killing it gives the memory back.
- **Memory:** 1024 MB total, 256 MB pre-used by the "system". `allocate` and `free` change a user-allocated counter and refuse requests that do not fit.
- **Users:** passwords are stored as SHA-256 hashes, not plain text.
- **Errors:** bad input prints a message instead of crashing the shell.
