from .tickets import get_ticket


def assign_ticket(tickets, ticket_id, staff):
    ticket = get_ticket(tickets, ticket_id)
    if ticket['status'] == 'resolved':
        raise ValueError('Reopen a resolved ticket before modifying it')
    if not isinstance(staff, str) or not staff.strip():
        raise ValueError('Staff name cannot be blank')
    ticket['assigned_to'] = staff.strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    ticket = get_ticket(tickets, ticket_id)
    new_status = new_status.strip().lower()
    current = ticket['status']
    valid = ((current == 'open' and new_status == 'in_progress' and ticket['assigned_to'])
             or (current == 'in_progress' and new_status == 'resolved')
             or (current == 'resolved' and new_status == 'open'))
    if not valid:
        raise ValueError('Invalid status change (assign before starting; reopen resolved tickets)')
    ticket['status'] = new_status
    return ticket


def work_queue(tickets):
    order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    return sorted((t for t in tickets if t['status'] == 'open'),
                  key=lambda t: (order[t['priority']], int(t['id'][1:])))
