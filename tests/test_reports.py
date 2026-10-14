"""Engineer B regression tests for enhanced reports."""

import unittest

from campusflow.reports import report


class ReportTests(unittest.TestCase):
    def test_empty_collection_is_safe(self):
        result = report([])
        self.assertEqual(result["total"], 0)
        self.assertEqual(result["unresolved"], 0)
        self.assertEqual(result["resolved"], 0)
        self.assertEqual(result["resolution_percentage"], 0.0)
        self.assertEqual(sum(result["category"].values()), 0)

    def test_counts_current_status_without_double_counting(self):
        tickets = [
            {"status": "open", "priority": "low", "category": "Network"},
            {"status": "in_progress", "priority": "high", "category": "Software"},
            {"status": "resolved", "priority": "critical", "category": "Network"},
            {"status": "open", "priority": "medium", "category": "Hardware"},
        ]
        result = report(tickets)
        self.assertEqual(result["total"], 4)
        self.assertEqual(result["unresolved"], 3)
        self.assertEqual(result["resolved"], 1)
        self.assertEqual(result["resolution_percentage"], 25.0)
        self.assertEqual(result["category"]["Network"], 2)
        self.assertEqual(sum(result["status"].values()), result["total"])

    def test_reopen_changes_current_counts(self):
        tickets = [{"status": "resolved", "priority": "high",
                    "category": "Other"}]
        self.assertEqual(report(tickets)["resolution_percentage"], 100.0)
        tickets[0]["status"] = "open"
        self.assertEqual(report(tickets)["resolution_percentage"], 0.0)
        self.assertEqual(report(tickets)["unresolved"], 1)


if __name__ == "__main__":
    unittest.main()
