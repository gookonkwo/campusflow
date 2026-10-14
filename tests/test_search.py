"""Tests for Engineer B's read-only combined search."""

import unittest

from campusflow.search import search_tickets


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {"id": "T001", "title": "WiFi outage", "category": "Network",
             "status": "open", "priority": "critical", "assigned_to": None},
            {"id": "T002", "title": "WiFi driver", "category": "Software",
             "status": "open", "priority": "medium", "assigned_to": None},
            {"id": "T003", "title": "Wifi router", "category": "Network",
             "status": "resolved", "priority": "high", "assigned_to": "A"},
        ]

    def test_title_search_ignores_case(self):
        self.assertEqual(
            [t["id"] for t in search_tickets(self.tickets, title="wIfI")],
            ["T001", "T002", "T003"])

    def test_combined_filters_require_every_match(self):
        found = search_tickets(self.tickets, title="wifi",
                               category="Network", status="open",
                               priority="critical")
        self.assertEqual([t["id"] for t in found], ["T001"])

    def test_empty_filters_return_all_in_original_order(self):
        self.assertEqual(search_tickets(self.tickets), self.tickets)

    def test_search_results_are_independent_deep_copies(self):
        from copy import deepcopy
        self.tickets[0]["notes"] = [{"id": "N001", "message": "Before"}]
        before = deepcopy(self.tickets)
        results = search_tickets(self.tickets, category="Network")
        self.assertIsNot(results[0], self.tickets[0])
        results[0]["title"] = "Changed outside storage"
        results[0]["notes"][0]["message"] = "Changed nested note"
        self.assertEqual(self.tickets, before)

    def test_invalid_filter_raises_without_changing_tickets(self):
        from copy import deepcopy
        before = deepcopy(self.tickets)
        with self.assertRaises(ValueError):
            search_tickets(self.tickets, status="deleted")
        self.assertEqual(self.tickets, before)

    def test_search_does_not_mutate_collection(self):
        from copy import deepcopy
        before = deepcopy(self.tickets)
        search_tickets(self.tickets, title="wifi", category="network")
        self.assertEqual(self.tickets, before)


if __name__ == "__main__":
    unittest.main()
