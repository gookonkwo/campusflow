"""Engineer A tests: validation boundaries and collection immutability."""

import copy
import unittest

from campusflow.tickets import create_ticket, get_ticket


class TicketValidationTests(unittest.TestCase):
    def test_invalid_affected_users_never_change_collection(self):
        tickets = [create_ticket([], "Temporary", "Network", "low", 1)]
        before = copy.deepcopy(tickets)
        for users in (0, -1, 2.5, True, False, "3", None):
            with self.subTest(users=users):
                with self.assertRaises(ValueError):
                    create_ticket(tickets, "Bad users", "Network", "high", users)
                self.assertEqual(tickets, before)

    def test_invalid_categories_and_urgencies_never_change_collection(self):
        tickets = []
        for category, urgency in (("Unknown", "low"), ("", "high"),
                                  (None, "medium"), ("Network", "urgent"),
                                  ("Hardware", ""), ("Software", None)):
            with self.subTest(category=category, urgency=urgency):
                before = copy.deepcopy(tickets)
                with self.assertRaises(ValueError):
                    create_ticket(tickets, "Problem", category, urgency, 2)
                self.assertEqual(tickets, before)

    def test_invalid_titles_do_not_consume_ticket_ids(self):
        tickets = []
        for title in ("", "   ", None, 42):
            with self.subTest(title=title):
                with self.assertRaises(ValueError):
                    create_ticket(tickets, title, "Network", "low", 1)
                self.assertEqual(tickets, [])
        self.assertEqual(create_ticket(tickets, "Valid", "Network", "low", 1)["id"], "T001")

    def test_invalid_ticket_id_raises_value_error_without_mutation(self):
        tickets = []
        create_ticket(tickets, "Valid", "Network", "low", 1)
        before = copy.deepcopy(tickets)
        for ticket_id in (None, 42, [], ""):
            with self.subTest(ticket_id=ticket_id):
                with self.assertRaises(ValueError):
                    get_ticket(tickets, ticket_id)
                self.assertEqual(tickets, before)


if __name__ == "__main__":
    unittest.main()
