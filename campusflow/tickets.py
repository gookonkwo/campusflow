CATEGORIES = {'network': 'Network', 'hardware': 'Hardware', 'software': 'Software', 'other': 'Other'}
URGENCIES = {'low', 'medium', 'high'}


def priority_for(urgency, affected_users):
    if urgency == 'high' and affected_users >= 10:
        return 'critical'
    if urgency == 'high' or affected_users >= 10:
        return 'high'
    if urgency == 'medium' or affected_users >= 3:
        return 'medium'
    return 'low'


def create_ticket(tickets, title, category, urgency, affected_users):
    if not isinstance(title, str) or not title.strip():
        raise ValueError('Title cannot be blank')
    if not isinstance(category, str) or category.strip().lower() not in CATEGORIES:
        raise ValueError('Category must be Network, Hardware, Software or Other')
    if not isinstance(urgency, str) or urgency.strip().lower() not in URGENCIES:
        raise ValueError('Urgency must be low, medium or high')
    if type(affected_users) is not int or affected_users <= 0:
        raise ValueError('Affected users must be a positive whole number')
    urgency = urgency.strip().lower()
    number = max((int(t['id'][1:]) for t in tickets), default=0) + 1
    ticket = {'id': f'T{number:03d}', 'title': title.strip(),
              'category': CATEGORIES[category.strip().lower()],
              'urgency': urgency, 'affected_users': affected_users,
              'priority': priority_for(urgency, affected_users),
              'status': 'open', 'assigned_to': None}
    tickets.append(ticket)
    return ticket


def get_ticket(tickets, ticket_id):
    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError('Ticket ID must be a nonblank string')
    normalized_id = ticket_id.strip().upper()
    for ticket in tickets:
        if ticket['id'] == normalized_id:
            return ticket
    raise ValueError('Unknown ticket ID')
