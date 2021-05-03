from event import Event
from datetime import date as Date


class Admin:
    def __init__(self):
        self.list_events: list = []

    def add_event(self, event: Event):
        self.list_events.append(event)

    def query_events(self):
        list_dates: list = []

        for event in self.list_events:
            if not event.date in list_dates:
                list_dates.append(event.date)

        list_return: list = []

        for date in list_dates:
            element = {}
            list_return.append(element)
            element['date'] = date.strftime('%d/%m/%Y')

            events_by_date = self.get_events_by_date(date)
            element['cant_events'] = len(events_by_date)

            user_reports: dict = {}

            for event in events_by_date:
                if not event.reported_by in user_reports:
                    user_reports[event.reported_by] = 1
                else:
                    user_reports[event.reported_by] = user_reports[
                        event.reported_by] + 1

            element['reported_by'] = []
            for user in user_reports.keys():
                element['reported_by'].append({
                    'email': user,
                    'cant': user_reports[user]
                })

            affected_users: list = []

            for event in events_by_date:
                for user in event.list_affected_users:
                    if not user in affected_users:
                        affected_users.append(user)

            element['affects'] = affected_users

            errors: dict = {}

            for event in events_by_date:
                if not event.error_code in errors:
                    errors[event.error_code] = 1
                else:
                    errors[event.error_code] = errors[event.error_code] + 1

            element['errors'] = []
            for error in errors.keys():
                element['errors'].append({
                    'code': error,
                    'cant': errors[error]
                })

        return list_return

    def get_events_by_date(self, date: Date):
        events: list = []

        for event in self.list_events:
            if event.date == date:
                events.append(event)

        return events

    def get_events_by_error(self, error_code: int):
        events: list = []
        for event in self.list_events:
            if event.error_code == int(error_code):
                events.append(event)

        return events

    def query_events_by_date(self, date: Date):
        events: list = self.get_events_by_date(date)

        list_users: dict = {}

        for event in events:
            if not event.reported_by in list_users:
                list_users[event.reported_by] = 1
            else:
                list_users[
                    event.reported_by] = list_users[event.reported_by] + 1

        list_return: list = []

        for user in list_users.keys():
            list_return.append({'user': user, 'cant': list_users[user]})

        return list_return

    def query_events_by_error_code(self, code: int):
        events: list = self.get_events_by_error(code)

        list_dates: dict = {}

        for event in events:
            if not event.date.strftime('%d/%m/%Y') in list_dates:
                list_dates[event.date.strftime('%d/%m/%Y')] = 1
            else:
                list_dates[event.date.strftime('%d/%m/%Y')] = list_dates[
                    event.date.strftime('%d/%m/%Y')] + 1

        list_return: list = []

        for date in list_dates.keys():
            list_return.append({'date': date, 'cant': list_dates[date]})

        return list_return

    # def get_events_order_by_date(self):
    #     list_dates: list = []

    #     for event in self.list_events:
    #         if not event.date in list_dates:
    #             list_dates.append(event.date)

    #     events_by_date: list = []

    #     for date in list_dates:
    #         element = {}
    #         element['date'] = date.strftime('%d/%m/%Y')
    #         element['events'] = self.get_events_by_date(date)
    #         events_by_date.append(element)

    #     return events_by_date

    # def get_events_by_date(self, date: Date):
    #     date_events: list = []

    #     for event in self.list_events:
    #         if event.date == date:
    #             date_events.append(event)

    #     return date_events

    # def get_events_by_reported_by(self, user: str):
    #     events: list = []

    #     for event in self.list_events:
    #         if event.reported_by == user:
    #             events.append(event)

    #     return events

    # def get_events_by_error(self, error_code: int):
    #     events: list = []

    #     for event in self.list_events:
    #         if event.error_code == int(error_code):
    #             events.append(event)

    #     return events
