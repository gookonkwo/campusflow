"""Engineer A regression tests for ticket lifecycle invariants.

These tests supplement the original workflow tests and assert collection-wide
immutability when a request is rejected.
"""

import copy
import unittest

from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status


class TicketSafetyRegressionTests(unittest.TestCase):
    def test_unassigned_open_ticket_cannot_start_and_collection_is_unchanged(self):
        tickets = []
        first = create_ticket(tickets, "Wi-Fi down", "Network", "high", 12)
        create_ticket(tickets, "Broken laptop", "Hardware", "low", 1)
        before = copy.deepcopy(tickets)

        with self.assertRaises(ValueError):
            change_status(tickets, first["id"], "in_progress")

        self.assertEqual(tickets, before)

    def test_resolved_ticket_reassignment_rejected_without_collection_mutation(self):
        tickets = []
        first = create_ticket(tickets, "Software update", "Software", "medium", 2)
        create_ticket(tickets, "Router issue", "Network", "low", 1)
        assign_ticket(tickets, first["id"], "Operator A")
        change_status(tickets, first["id"], "in_progress")
        change_status(tickets, first["id"], "resolved")
        before = copy.deepcopy(tickets)

        with self.assertRaises(ValueError):
            assign_ticket(tickets, first["id"], "Operator B")

        self.assertEqual(tickets, before)

    def test_reopened_ticket_can_be_assigned_again(self):
        tickets = []
        ticket = create_ticket(tickets, "Projector issue", "Hardware", "low", 1)
        assign_ticket(tickets, ticket["id"], "Operator A")
        change_status(tickets, ticket["id"], "in_progress")
        change_status(tickets, ticket["id"], "resolved")
        change_status(tickets, ticket["id"], "open")

        result = assign_ticket(tickets, ticket["id"], "Operator B")
        self.assertEqual(result["assigned_to"], "Operator B")
        self.assertEqual(result["status"], "open")


if __name__ == "__main__":
    unittest.main()
