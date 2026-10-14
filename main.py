"""CampusFlow command-line helpdesk; Python standard library only."""
import argparse
from copy import deepcopy
from pathlib import Path
import sys

from campusflow.tickets import create_ticket, get_ticket
from campusflow.workflow import assign_ticket, change_status, work_queue
from campusflow.reports import report
from campusflow.search import search_tickets, CATEGORIES, STATUSES, PRIORITIES
from campusflow.understanding_check import run_understanding_check
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
8. Search tickets
9. Engineering Understanding Check
10. Add follow-up note
11. View ticket notes
12. Exit'''


def show(tickets):
    if not tickets:
        print('No tickets found.')
    for ticket in tickets:
        print(f"{ticket['id']} | {ticket['title']} | {ticket['priority']} | "
              f"{ticket['status']} | {ticket['assigned_to'] or 'Unassigned'}")


def ask_filter(label, allowed):
    """Return a valid optional filter; blank means all."""
    while True:
        value = input(f'{label} ({"/".join(allowed)}; blank=all): ').strip()
        if not value or value.casefold() in {item.casefold() for item in allowed}:
            return value
        print(f'Invalid {label.lower()}. Please try again.')


def show_search_results(tickets):
    if not tickets:
        print('No tickets found.')
    for ticket in tickets:
        print(f"{ticket['id']} | {ticket['title']} | {ticket['category']} | "
              f"{ticket['priority']} | {ticket['status']} | "
              f"{ticket['assigned_to'] or 'Unassigned'}")


def show_report(tickets):
    summary = report(tickets)
    print(f"Total tickets: {summary['total']}")
    for group in ('status', 'priority', 'category'):
        print(f'{group.capitalize()}:')
        for name, count in summary[group].items():
            print(f'  {name}: {count}')
    print(f"Unresolved: {summary['unresolved']}")
    print(f"Resolved: {summary['resolved']}")
    print(f"Resolution percentage: {summary['resolution_percentage']:.2f}%")


def add_note_cli(tickets, path):
    """Use Engineer A's note API; save only after successful validation."""
    from campusflow.notes import add_note
    candidate = deepcopy(tickets)
    ticket_id = input('Ticket ID: ')
    author = input('Author: ')
    message = input('Note message: ')
    note = add_note(candidate, ticket_id, author, message)
    save_tickets(candidate, path)
    print(f"Saved note {note['note_id']} for {ticket_id}.")
    return candidate


def view_notes_cli(tickets):
    ticket = get_ticket(tickets, input('Ticket ID: '))
    notes = ticket.get('notes', [])
    if not notes:
        print('No notes for this ticket.')
    for note in sorted(notes, key=lambda item: int(item['note_id'][1:])):
        print(f"{note['note_id']} | {note['author']} | {note['message']}")


def run(path):
    try:
        tickets = load_tickets(path)
    except (ValueError, OSError) as error:
        print(f'Startup error: {error}. Existing data was preserved.', file=sys.stderr)
        return 1
    while True:
        try:
            print(MENU)
            choice = input('Choose 1–12: ').strip()
            if choice == '12':
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
                show_report(tickets)
            elif choice == '8':
                title = input('Title contains (blank=all): ')
                category = ask_filter('Category', CATEGORIES)
                status = ask_filter('Status', STATUSES)
                priority = ask_filter('Priority', PRIORITIES)
                show_search_results(search_tickets(
                    tickets, title=title, category=category,
                    status=status, priority=priority))
            elif choice == '9':
                run_understanding_check()
            elif choice == '10':
                tickets = add_note_cli(tickets, path)
            elif choice == '11':
                view_notes_cli(tickets)
            else:
                print('Please choose a number from 1 to 12.')
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
