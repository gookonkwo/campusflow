"""Structured follow-up notes for CampusFlow tickets."""

from .tickets import get_ticket


def add_note(tickets, ticket_id, author, message):
    """Append a validated note and return it; reject requests before mutation."""
    ticket = get_ticket(tickets, ticket_id)
    if ticket["status"] == "resolved":
        raise ValueError("Reopen a resolved ticket before adding notes")
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be blank")
    if not isinstance(message, str) or not message.strip():
        raise ValueError("Note message cannot be blank")

    existing = ticket.get("notes", [])
    if not isinstance(existing, list):
        raise ValueError("Ticket notes must be a list")
    seen = set()
    numbers = []
    for prior in existing:
        if not isinstance(prior, dict):
            raise ValueError("Existing note must be an object")
        ident = prior.get("id")
        if (not isinstance(ident, str) or len(ident) < 2
                or not ident.startswith("N") or not ident[1:].isdigit()
                or int(ident[1:]) < 1 or ident in seen):
            raise ValueError("Existing note has an invalid or duplicate ID")
        seen.add(ident)
        numbers.append(int(ident[1:]))
    number = max(numbers, default=0) + 1
    note = {"id": f"N{number:03d}", "author": author.strip(),
            "message": message.strip()}
    if "notes" not in ticket:
        ticket["notes"] = []
    ticket["notes"].append(note)
    return note
