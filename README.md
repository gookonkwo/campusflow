# CampusFlow — CLI Helpdesk

A Python command-line system for recording campus technical support tickets, ordering work by priority, assigning staff, tracking status, and saving data to JSON.

## Team
Engineer A: [your name] — ticket creation, validation, priority and tests.
Engineer B: [partner name] — assignment, workflow, queue, reports and tests.
**Edit this section to reflect actual contributions, not planned roles.**

## Requirements
Python 3.9+; no external packages needed.

## Run
```bash
python main.py
```
Choose menu items 1–8. Tickets are saved in `data/tickets.json` automatically after changes. To start fresh, remove that file when the program is closed.

## Test
```bash
python -m unittest discover -s tests -v
```

## Rules
- Priority: high + at least 10 users = critical; high urgency or 10+ users = high; medium urgency or 3+ users = medium; otherwise low.
- Workflow: open → in_progress (only if assigned) → resolved. Resolved tickets must be reopened before modification.
- Queue: only open tickets; sorted by priority, then numeric ID.
- Invalid JSON causes a startup error instead of silently deleting saved tickets.

## Known limitations
- Local single-user CLI only; no concurrency, authentication or graphical interface.
- Saved JSON is checked for required fields and unique IDs but not all schema value types.

## GitHub review evidence
Engineer A PR: [add link after genuine review]
Engineer B PR: [add link after genuine review]
