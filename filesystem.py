"""filesystem.py - A virtual, in-memory file system for MiniOS.

Nothing here touches the real disk. Directories and files live in a tree
of Python objects, which keeps the simulation safe and easy to explain.
"""

from datetime import datetime


class Node:
    def __init__(self, name, is_dir, parent=None):
        self.name = name
        self.is_dir = is_dir
        self.parent = parent
        self.content = ""
        self.children = {}
        self.created = datetime.now()


class FileSystem:
    def __init__(self):
        self.root = Node("", True)
        self.cwd = self.root

    # ---- helpers -------------------------------------------------------
    def path(self, node=None):
        node = node or self.cwd
        parts = []
        while node is not None and node.parent is not None:
            parts.append(node.name)
            node = node.parent
        return "\\" + "\\".join(reversed(parts))

    @staticmethod
    def _valid_name(name):
        bad = set('\\/:*?"<>|')
        return bool(name) and not any(c in bad for c in name) and name not in (".", "..")

    def _resolve(self, path):
        """Walk a path like 'Docs\\sub' or '..' and return a node, or None."""
        node = self.root if path.startswith(("\\", "/")) else self.cwd
        for part in path.replace("/", "\\").split("\\"):
            if part in ("", "."):
                continue
            if part == "..":
                node = node.parent or node
                continue
            if not node.is_dir or part not in node.children:
                return None
            node = node.children[part]
        return node

    # ---- commands ------------------------------------------------------
    def listing(self):
        """Return a list of (name, is_dir, size) for the current directory."""
        items = sorted(self.cwd.children.values(), key=lambda n: (not n.is_dir, n.name.lower()))
        return [(n.name, n.is_dir, len(n.content)) for n in items]

    def mkdir(self, name):
        if not self._valid_name(name):
            return "Error: Invalid directory name."
        if name in self.cwd.children:
            return "Error: A file or directory with that name already exists."
        self.cwd.children[name] = Node(name, True, self.cwd)
        return "Directory created."

    def create(self, name):
        if not self._valid_name(name):
            return "Error: Invalid file name."
        if name in self.cwd.children:
            return "Error: A file or directory with that name already exists."
        self.cwd.children[name] = Node(name, False, self.cwd)
        return "File created."

    def read(self, name):
        node = self.cwd.children.get(name)
        if node is None:
            return "Error: File does not exist."
        if node.is_dir:
            return "Error: That is a directory, not a file."
        return node.content if node.content else "(file is empty)"

    def write(self, name, text, append=False):
        node = self.cwd.children.get(name)
        if node is None:
            return "Error: File does not exist."
        if node.is_dir:
            return "Error: That is a directory, not a file."
        node.content = node.content + text if append else text
        return "File updated."

    def delete(self, name):
        node = self.cwd.children.get(name)
        if node is None:
            return "Error: File or directory does not exist."
        if node.is_dir:
            if node.children:
                return "Error: Directory is not empty."
            del self.cwd.children[name]
            return "Directory deleted."
        del self.cwd.children[name]
        return "File deleted."

    def rename(self, old, new):
        if old not in self.cwd.children:
            return "Error: File or directory does not exist."
        if not self._valid_name(new):
            return "Error: Invalid new name."
        if new in self.cwd.children:
            return "Error: A file or directory with that name already exists."
        node = self.cwd.children.pop(old)
        node.name = new
        self.cwd.children[new] = node
        return "Renamed."

    def cd(self, path):
        node = self._resolve(path)
        if node is None:
            return "Error: Directory does not exist."
        if not node.is_dir:
            return "Error: That is a file, not a directory."
        self.cwd = node
        return ""
