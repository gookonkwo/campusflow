"""Engineer B CLI integration tests with mocked inputs and dependencies."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main


class CliTests(unittest.TestCase):
    def test_invalid_filter_retries(self):
        with patch("builtins.input", side_effect=["wrong", "network"]):
            output = io.StringIO()
            with redirect_stdout(output):
                result = main.ask_filter("Category", ("Network", "Hardware"))
        self.assertEqual(result, "network")
        self.assertIn("Invalid category", output.getvalue())

    def test_search_output_has_required_fields(self):
        tickets = [{"id": "T001", "title": "WiFi", "category": "Network",
                    "priority": "high", "status": "open", "assigned_to": None}]
        output = io.StringIO()
        with redirect_stdout(output):
            main.show_search_results(tickets)
        for value in ("T001", "WiFi", "Network", "high", "open", "Unassigned"):
            self.assertIn(value, output.getvalue())

    def test_empty_report_prints_zero_percent(self):
        output = io.StringIO()
        with redirect_stdout(output):
            main.show_report([])
        self.assertIn("Resolution percentage: 0.00%", output.getvalue())

    def test_add_note_persists_across_restart(self):
        from campusflow.tickets import create_ticket
        from campusflow.storage import save_tickets, load_tickets
        from campusflow.notes import add_note
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            tickets = []
            ticket = create_ticket(tickets, "WiFi down", "Network", "high", 10)
            save_tickets(tickets, path)
            with patch("builtins.input", side_effect=[ticket["id"], "Ada", "Checked router"]):
                with redirect_stdout(io.StringIO()):
                    updated = main.add_note_cli(load_tickets(path), path)
            self.assertEqual(updated[0]["notes"][0]["id"], "N001")
            reloaded = load_tickets(path)
            self.assertEqual(reloaded[0]["notes"][0]["message"], "Checked router")
            next_note = add_note(reloaded, ticket["id"], "Ben", "Restarted router")
            self.assertEqual(next_note["id"], "N002")

    def test_rejected_note_does_not_overwrite_file(self):
        from campusflow.tickets import create_ticket
        from campusflow.storage import save_tickets, load_tickets
        from campusflow.workflow import assign_ticket, change_status
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "tickets.json"
            tickets = []
            ticket = create_ticket(tickets, "WiFi down", "Network", "high", 10)
            assign_ticket(tickets, ticket["id"], "Ada")
            change_status(tickets, ticket["id"], "in_progress")
            change_status(tickets, ticket["id"], "resolved")
            save_tickets(tickets, path)
            before = path.read_bytes()
            with patch("builtins.input", side_effect=[ticket["id"], "Ben", "Late note"]):
                with self.assertRaises(ValueError):
                    main.add_note_cli(load_tickets(path), path)
            self.assertEqual(path.read_bytes(), before)

    def test_view_notes_in_numeric_id_order(self):
        tickets = [{"id": "T001", "notes": [
            {"id": "N010", "author": "B", "message": "Second"},
            {"id": "N002", "author": "A", "message": "First"}]}]
        output = io.StringIO()
        with patch("builtins.input", return_value="T001"):
            with redirect_stdout(output):
                main.view_notes_cli(tickets)
        self.assertLess(output.getvalue().index("N002"),
                        output.getvalue().index("N010"))


if __name__ == "__main__":
    unittest.main()
