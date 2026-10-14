"""Read-only aggregate ticket reports."""


def report(tickets):
    """Count tickets by their current state, including empty collections."""
    total = len(tickets)
    status = {name: sum(t["status"] == name for t in tickets)
              for name in ("open", "in_progress", "resolved")}
    priority = {name: sum(t["priority"] == name for t in tickets)
                for name in ("critical", "high", "medium", "low")}
    category = {name: sum(t["category"] == name for t in tickets)
                for name in ("Network", "Hardware", "Software", "Other")}
    resolved = status["resolved"]
    return {
        "total": total,
        "status": status,
        "priority": priority,
        "category": category,
        "unresolved": status["open"] + status["in_progress"],
        "resolved": resolved,
        "resolution_percentage": resolved / total * 100 if total else 0.0,
    }
