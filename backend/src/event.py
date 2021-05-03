from datetime import date as Date


class Event:
    def __init__(self, date: Date, reported_by: str, error_code: int):
        self.date: Date = date
        self.reported_by: str = reported_by
        self.error_code: int = error_code

        self.list_affected_users: list = []

    def add_affected_user(self, user: str):
        self.list_affected_users.append(user)

    # def __repr__(self):
    #     return '{' + '"date": "{}",\n"reported_by": "{}",\n"error_code": "{}"\n,"affected_users": {}'.format(
    #         self.date.strftime('%d/%m/%Y'), self.reported_by, self.error_code,
    #         self.list_affected_users) + '}'
