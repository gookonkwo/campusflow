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

    def test_view_notes_in_numeric_id_order(self):
        tickets = [{"id": "T001", "notes": [
            {"note_id": "N010", "author": "B", "message": "Second"},
            {"note_id": "N002", "author": "A", "message": "First"}]}]
        output = io.StringIO()
        with patch("builtins.input", return_value="T001"):
            with redirect_stdout(output):
                main.view_notes_cli(tickets)
        self.assertLess(output.getvalue().index("N002"),
                        output.getvalue().index("N010"))


if __name__ == "__main__":
    unittest.main()
