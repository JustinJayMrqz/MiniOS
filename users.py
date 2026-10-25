"""users.py - User management for MiniOS.

Handles the account list, password checks (stored as SHA-256 hashes,
never as plain text) and the currently logged-in user.
"""

import getpass
import hashlib


def _hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class UserManager:
    def __init__(self):
        # username -> {"password": hash, "role": role}
        self.accounts = {
            "admin": {"password": _hash("admin123"), "role": "Administrator"},
            "student": {"password": _hash("student123"), "role": "Standard User"},
        }
        self.current_user = None

    def authenticate(self, username, password):
        """Return True and set the current user if the credentials match."""
        account = self.accounts.get(username)
        if account and account["password"] == _hash(password):
            self.current_user = username
            return True
        return False

    def login_prompt(self, max_attempts=3):
        """Ask for credentials. Returns True on success, False after too many failures."""
        print("=" * 40)
        print("              MiniOS Login")
        print("=" * 40)
        for attempt in range(1, max_attempts + 1):
            try:
                username = input("Username: ").strip()
                try:
                    password = getpass.getpass("Password: ")
                except Exception:
                    password = input("Password: ")
            except (EOFError, KeyboardInterrupt):
                print()
                return False
            if self.authenticate(username, password):
                print("\nLogin successful.\n")
                print(f"Welcome, {username}!\n")
                return True
            left = max_attempts - attempt
            print(f"\nError: Invalid username or password. ({left} attempt(s) left)\n")
        return False

    def logout(self):
        self.current_user = None

    def role(self):
        if self.current_user is None:
            return "None"
        return self.accounts[self.current_user]["role"]

    def is_admin(self):
        return self.role() == "Administrator"

    def list_users(self):
        return [(name, data["role"]) for name, data in self.accounts.items()]
