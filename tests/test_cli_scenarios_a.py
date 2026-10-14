"""Scripted CLI regression scenarios for Engineer A's workflow checks.

These exercise the actual menu through mocked user input and temporary JSON files.
They are automated reproductions, not evidence of interactive manual execution.
"""
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from main import run
from campusflow.storage import load_tickets


class WorkflowCliScenarioTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "tickets.json"

    def play(self, answers):
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), patch("sys.stdout", output):
            result = run(self.path)
        self.assertEqual(result, 0)
        return output.getvalue()

    def test_high_urgency_ten_users_is_critical(self):
        self.play(["1", "Wi-Fi outage", "Network", "high", "10", "8"])
        ticket = load_tickets(self.path)[0]
        self.assertEqual(ticket["priority"], "critical")

    def test_unassigned_in_progress_is_rejected_without_mutation(self):
        output = self.play(["1", "Wi-Fi outage", "Network", "high", "10",
                            "5", "T001", "in_progress", "8"])
        self.assertIn("Error:", output)
        ticket = load_tickets(self.path)[0]
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_resolved_reassignment_rejected_then_reopen_succeeds(self):
        output = self.play(["1", "Wi-Fi outage", "Network", "high", "10",
                            "4", "T001", "Operator A",
                            "5", "T001", "in_progress",
                            "5", "T001", "resolved",
                            "4", "T001", "Operator B",
                            "5", "T001", "open", "8"])
        self.assertIn("Error:", output)
        ticket = load_tickets(self.path)[0]
        self.assertEqual(ticket["assigned_to"], "Operator A")
        self.assertEqual(ticket["status"], "open")


if __name__ == "__main__":
    unittest.main()
