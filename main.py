"""CampusFlow command-line helpdesk; Python standard library only."""
import argparse
from copy import deepcopy
from pathlib import Path
import sys

from campusflow.tickets import create_ticket, get_ticket
from campusflow.workflow import assign_ticket, change_status, work_queue
from campusflow.reports import report
from campusflow.storage import load_tickets, save_tickets

MENU = '''
CampusFlow
1. Create ticket
2. List tickets
3. View ticket
4. Assign staff
5. Change status / reopen
6. Work queue
7. Reports
8. Exit'''


def show(tickets):
    if not tickets:
        print('No tickets found.')
    for ticket in tickets:
        print(f"{ticket['id']} | {ticket['title']} | {ticket['priority']} | "
              f"{ticket['status']} | {ticket['assigned_to'] or 'Unassigned'}")


def run(path):
    try:
        tickets = load_tickets(path)
    except (ValueError, OSError) as error:
        print(f'Startup error: {error}. Existing data was preserved.', file=sys.stderr)
        return 1
    while True:
        try:
            print(MENU)
            choice = input('Choose 1–8: ').strip()
            if choice == '8':
                print('Goodbye!')
                return 0
            if choice in ('1', '4', '5'):
                candidate = deepcopy(tickets)
                if choice == '1':
                    title = input('Title: ')
                    category = input('Category (Network/Hardware/Software/Other): ')
                    urgency = input('Urgency (low/medium/high): ')
                    users = int(input('Affected users: '))
                    changed = create_ticket(candidate, title, category, urgency, users)
                elif choice == '4':
                    ident = input('Ticket ID: ')
                    changed = assign_ticket(candidate, ident, input('Staff name: '))
                else:
                    ident = input('Ticket ID: ')
                    changed = change_status(candidate, ident, input('Status (open/in_progress/resolved): '))
                save_tickets(candidate, path)
                tickets = candidate
                print(f"Saved {changed['id']}.")
            elif choice == '2':
                show(tickets)
            elif choice == '3':
                ticket = get_ticket(tickets, input('Ticket ID: '))
                for field, value in ticket.items():
                    print(f'{field}: {value}')
            elif choice == '6':
                show(work_queue(tickets))
            elif choice == '7':
                summary = report(tickets)
                print(f"Total tickets: {summary['total']}")
                for group in ('status', 'priority'):
                    print(f'{group.capitalize()}:')
                    for name, count in summary[group].items():
                        print(f'  {name}: {count}')
            else:
                print('Please choose a number from 1 to 8.')
        except (ValueError, OSError) as error:
            print(f'Error: {error}')
        except (EOFError, KeyboardInterrupt):
            print('\nGoodbye!')
            return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CampusFlow CLI helpdesk')
    parser.add_argument('--data', type=Path,
                        default=Path(__file__).resolve().parent / 'data' / 'tickets.json',
                        help='JSON file for persistent tickets')
    sys.exit(run(parser.parse_args().data))
