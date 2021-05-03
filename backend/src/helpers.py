from event import Event


def parse_list_users(csv_line: str):
    parse_users: list = []
    for element in csv_line.split(','):
        parse_users.append(element.strip())
        # parse_users.append(element.strip().replace(',', ''))

    return parse_users


def serialize_event(event: Event):
    return {
        'date': event.date.strftime('%d/%m/%Y'),
        'reported_by': event.reported_by,
        'affected_users': event.list_affected_users,
        'error_code': event.error_code
    }