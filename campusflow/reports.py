def report(tickets):
    return {
        'total': len(tickets),
        'status': {s: sum(t['status'] == s for t in tickets)
                   for s in ('open', 'in_progress', 'resolved')},
        'priority': {p: sum(t['priority'] == p for t in tickets)
                     for p in ('critical', 'high', 'medium', 'low')},
    }
