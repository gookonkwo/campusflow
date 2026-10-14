"""Read-only ticket search with combined optional filters."""

CATEGORIES = ("Network", "Hardware", "Software", "Other")
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")


def search_tickets(tickets, title="", category="", status="", priority=""):
    """Return tickets matching ALL supplied filters, without changing the source.

    Empty strings mean no filter. Category is matched case-insensitively;
    status and priority use their canonical lowercase names.
    """
    filters = (("title", title), ("category", category),
               ("status", status), ("priority", priority))
    for name, value in filters:
        if not isinstance(value, str):
            raise ValueError(f"{name} filter must be text")
    title = title.strip().casefold()
    category = category.strip().casefold()
    status = status.strip().casefold()
    priority = priority.strip().casefold()
    if category and category not in {x.casefold() for x in CATEGORIES}:
        raise ValueError("Invalid category filter")
    if status and status not in STATUSES:
        raise ValueError("Invalid status filter")
    if priority and priority not in PRIORITIES:
        raise ValueError("Invalid priority filter")

    return [
        ticket for ticket in tickets
        if (not title or title in ticket["title"].casefold())
        and (not category or category == ticket["category"].casefold())
        and (not status or status == ticket["status"])
        and (not priority or priority == ticket["priority"])
    ]
