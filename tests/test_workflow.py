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
