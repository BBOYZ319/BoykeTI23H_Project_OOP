from abc import ABC, abstractmethod

class AbstractUser(ABC):
    @abstractmethod
    def display_info(self):
        pass

class User:
    def __init__(self, user_id, username, password=None):
        self.user_id = user_id
        self.username = username
        self.password = password


    def display_info(self):
        print(f"[CLIENT] Aktif sebagai user: {self.username}")
