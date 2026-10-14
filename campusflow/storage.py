"""Validated JSON storage with atomic replacement."""
import json
import os
from pathlib import Path
import re
import tempfile

from .tickets import CATEGORIES, URGENCIES, priority_for


def validate(tickets):
    if not isinstance(tickets, list):
        raise ValueError('Saved tickets must be a list')
    seen = set()
    required = {'id', 'title', 'category', 'urgency', 'affected_users',
                'priority', 'status', 'assigned_to'}
    for ticket in tickets:
        if not isinstance(ticket, dict) or not required.issubset(ticket):
            raise ValueError('Saved ticket has missing fields')
        ident = ticket['id']
        if not isinstance(ident, str) or not re.fullmatch(r'T[0-9]{3,}', ident):
            raise ValueError('Invalid saved ticket ID')
        number = int(ident[1:])
        if number < 1 or number in seen:
            raise ValueError('Duplicate or invalid saved ticket ID')
        seen.add(number)
        if not isinstance(ticket['title'], str) or not ticket['title'].strip():
            raise ValueError('Invalid saved title')
        if ticket['category'] not in tuple(CATEGORIES.values()):
            raise ValueError('Invalid saved category')
        if not isinstance(ticket['urgency'], str) or ticket['urgency'] not in URGENCIES:
            raise ValueError('Invalid saved urgency')
        users = ticket['affected_users']
        if type(users) is not int or users < 1:
            raise ValueError('Invalid saved affected user count')
        if ticket['priority'] != priority_for(ticket['urgency'], users):
            raise ValueError('Saved priority does not match urgency and users')
        if ticket['status'] not in ('open', 'in_progress', 'resolved'):
            raise ValueError('Invalid saved status')
        staff = ticket['assigned_to']
        if staff is not None and (not isinstance(staff, str) or not staff.strip()):
            raise ValueError('Invalid saved staff name')
        if ticket['status'] != 'open' and staff is None:
            raise ValueError('Started tickets must have assigned staff')
        notes = ticket.get('notes', [])
        if not isinstance(notes, list):
            raise ValueError('Saved notes must be a list')
        note_numbers = set()
        for note in notes:
            if not isinstance(note, dict) or not {'id', 'author', 'message'}.issubset(note):
                raise ValueError('Invalid saved note structure')
            note_id = note['id']
            if not isinstance(note_id, str) or not re.fullmatch(r'N[0-9]{3,}', note_id):
                raise ValueError('Invalid saved note ID')
            note_number = int(note_id[1:])
            if note_number < 1 or note_number in note_numbers:
                raise ValueError('Duplicate or invalid saved note ID')
            note_numbers.add(note_number)
            for field in ('author', 'message'):
                if not isinstance(note[field], str) or not note[field].strip():
                    raise ValueError('Invalid saved note ' + field)
    return tickets


def load_tickets(path):
    path = Path(path)
    try:
        with path.open(encoding='utf-8') as source:
            return validate(json.load(source))
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeError) as error:
        raise ValueError('Cannot read saved tickets: invalid JSON') from error


def save_tickets(tickets, path):
    validate(tickets)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                         dir=path.parent, delete=False) as target:
            temporary = target.name
            json.dump(tickets, target, indent=2, ensure_ascii=False)
            target.write('\n')
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and os.path.exists(temporary):
            os.unlink(temporary)
