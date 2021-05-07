from datetime import date as Date


class Event:
    def __init__(self, date: Date, reported_by: str, error_code: int):
        self.date: Date = date
        self.reported_by: str = reported_by
        self.error_code: int = error_code

        self.list_affected_users: list = []

    def add_affected_user(self, user: str):
        self.list_affected_users.append(user)
