import unittest
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status, work_queue
from campusflow.reports import report


def new(tickets, urgency='low', users=1):
    return create_ticket(tickets, 'Help', 'Network', urgency, users)


class WorkflowTests(unittest.TestCase):
    def test_unassigned_cannot_start(self):
        tickets = []
        ticket = new(tickets)
        with self.assertRaises(ValueError): change_status(tickets, ticket['id'], 'in_progress')
        self.assertEqual(ticket['status'], 'open')
    def test_assigned_can_resolve_and_reopen(self):
        tickets = []
        ticket = new(tickets)
        assign_ticket(tickets, ticket['id'], 'Ada')
        change_status(tickets, ticket['id'], 'in_progress')
        change_status(tickets, ticket['id'], 'resolved')
        self.assertEqual(ticket['status'], 'resolved')
        change_status(tickets, ticket['id'], 'open')
        self.assertEqual(ticket['status'], 'open')
    def test_queue_priority_and_id(self):
        tickets = []
        a = new(tickets, 'low', 1)
        b = new(tickets, 'high', 12)
        c = new(tickets, 'high', 12)
        self.assertEqual([t['id'] for t in work_queue(tickets)], [b['id'], c['id'], a['id']])
    def test_resolved_cannot_assign(self):
        tickets = []
        t = new(tickets)
        assign_ticket(tickets, t['id'], 'Ada')
        change_status(tickets, t['id'], 'in_progress')
        change_status(tickets, t['id'], 'resolved')
        with self.assertRaises(ValueError): assign_ticket(tickets, t['id'], 'Bob')
    def test_empty_report(self): self.assertEqual(report([])['total'], 0)
    def test_unknown_id(self):
        with self.assertRaises(ValueError): assign_ticket([], 'T999', 'Ada')


class WorkflowEdgeTests(unittest.TestCase):
    def test_blank_staff_preserves_assignment(self):
        tickets = []
        ticket = new(tickets)
        assign_ticket(tickets, ticket['id'], 'Ada')
        for staff in ('', '  ', None):
            with self.subTest(staff=staff):
                before = ticket.copy()
                with self.assertRaises(ValueError):
                    assign_ticket(tickets, ticket['id'], staff)
                self.assertEqual(ticket, before)

    def test_invalid_status_preserves_ticket(self):
        tickets = []
        ticket = new(tickets)
        for status in ('resolved', 'open', 'unknown', '', None, 42):
            with self.subTest(status=status):
                before = ticket.copy()
                with self.assertRaises(ValueError):
                    change_status(tickets, ticket['id'], status)
                self.assertEqual(ticket, before)

    def test_queue_excludes_started_and_resolved(self):
        tickets = []
        waiting = new(tickets)
        started = new(tickets, 'high', 12)
        resolved = new(tickets, 'high', 12)
        for ticket in (started, resolved):
            assign_ticket(tickets, ticket['id'], 'Ada')
            change_status(tickets, ticket['id'], 'in_progress')
        change_status(tickets, resolved['id'], 'resolved')
        self.assertEqual(work_queue(tickets), [waiting])
        change_status(tickets, resolved['id'], 'open')
        self.assertEqual(work_queue(tickets), [resolved, waiting])

    def test_report_counts_mixed_tickets(self):
        tickets = []
        new(tickets)
        high = new(tickets, 'high', 1)
        critical = new(tickets, 'high', 10)
        for ticket in (high, critical):
            assign_ticket(tickets, ticket['id'], 'Ada')
            change_status(tickets, ticket['id'], 'in_progress')
        change_status(tickets, critical['id'], 'resolved')
        self.assertEqual(report(tickets), {
            'total': 3,
            'status': {'open': 1, 'in_progress': 1, 'resolved': 1},
            'priority': {'critical': 1, 'high': 1, 'medium': 0, 'low': 1},
            'category': {'Network': 3, 'Hardware': 0, 'Software': 0, 'Other': 0},
            'unresolved': 2,
            'resolved': 1,
            'resolution_percentage': 100 / 3,
        })
