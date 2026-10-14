"""Regression tests for persisted ticket notes and ID continuity."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from campusflow.notes import add_note
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket


class NoteStorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "tickets.json"
        self.tickets = []
        self.ticket = create_ticket(self.tickets, "Wi-Fi", "Network", "high", 10)

    def test_new_ticket_has_empty_notes_list(self):
        self.assertEqual(self.ticket["notes"], [])

    def test_round_trip_preserves_notes_and_next_note_id(self):
        add_note(self.tickets, self.ticket["id"], "Ada", "Checked router")
        add_note(self.tickets, self.ticket["id"], "Ada", "Restarted router")
        save_tickets(self.tickets, self.path)
        loaded = load_tickets(self.path)
        self.assertEqual(loaded, self.tickets)
        self.assertEqual(add_note(loaded, self.ticket["id"], "Bob", "Confirmed")["id"], "N003")
        self.assertEqual(create_ticket(loaded, "Printer", "Hardware", "low", 1)["id"], "T002")

    def test_invalid_saved_notes_rejected_without_overwriting_file(self):
        valid = copy.deepcopy(self.tickets[0])
        for notes in (None, {}, "notes", [42],
                      [{"id": "N000", "author": "Ada", "message": "Done"}],
                      [{"id": "N001", "author": "", "message": "Done"}],
                      [{"id": "N001", "author": "Ada", "message": ""}],
                      [{"id": "N001", "author": "Ada", "message": "A"},
                       {"id": "N001", "author": "Bob", "message": "B"}]):
            with self.subTest(notes=notes):
                bad = dict(valid, notes=notes)
                raw = json.dumps([bad])
                self.path.write_text(raw, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_tickets(self.path)
                self.assertEqual(self.path.read_text(encoding="utf-8"), raw)

    def test_invalid_notes_rejected_before_save_replaces_existing_data(self):
        save_tickets(self.tickets, self.path)
        before = self.path.read_bytes()
        self.ticket["notes"] = [{"id": "N001", "author": "Ada", "message": " "}]
        with self.assertRaises(ValueError):
            save_tickets(self.tickets, self.path)
        self.assertEqual(self.path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
