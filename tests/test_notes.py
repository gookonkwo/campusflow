"""Engineer A: notes business rules, identity, and mutation-safety tests."""
import copy
import unittest

from campusflow.notes import add_note
from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status


class NoteTests(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        self.ticket = create_ticket(self.tickets, "Wi-Fi down", "Network", "high", 10)

    def test_add_note_returns_structured_note_and_stores_it(self):
        note = add_note(self.tickets, self.ticket["id"], " Ada ", " Restarted router ")
        self.assertEqual(note, {"id": "N001", "author": "Ada", "message": "Restarted router"})
        self.assertEqual(self.ticket["notes"], [note])

    def test_note_ids_increment_per_ticket(self):
        first = add_note(self.tickets, self.ticket["id"], "Ada", "First")
        second = add_note(self.tickets, self.ticket["id"], "Ada", "Second")
        other = create_ticket(self.tickets, "Printer", "Hardware", "low", 1)
        third = add_note(self.tickets, other["id"], "Bob", "Independent")
        self.assertEqual((first["id"], second["id"], third["id"]), ("N001", "N002", "N001"))

    def test_invalid_author_message_and_ticket_id_do_not_mutate(self):
        for ticket_id, author, message in (
            (self.ticket["id"], "", "Update"),
            (self.ticket["id"], None, "Update"),
            (self.ticket["id"], "Ada", " "),
            (self.ticket["id"], "Ada", None),
            ("T999", "Ada", "Update"),
        ):
            with self.subTest(ticket_id=ticket_id, author=author, message=message):
                before = copy.deepcopy(self.tickets)
                with self.assertRaises(ValueError):
                    add_note(self.tickets, ticket_id, author, message)
                self.assertEqual(self.tickets, before)

    def test_resolved_ticket_rejects_notes_without_mutation(self):
        assign_ticket(self.tickets, self.ticket["id"], "Ada")
        change_status(self.tickets, self.ticket["id"], "in_progress")
        change_status(self.tickets, self.ticket["id"], "resolved")
        before = copy.deepcopy(self.tickets)
        with self.assertRaises(ValueError):
            add_note(self.tickets, self.ticket["id"], "Ada", "Late update")
        self.assertEqual(self.tickets, before)

    def test_malformed_existing_note_ids_do_not_mutate(self):
        malformed = (
            [{"author": "Ada", "message": "Missing ID"}],
            [{"id": None, "author": "Ada", "message": "Invalid ID"}],
            [{"id": "broken", "author": "Ada", "message": "Invalid ID"}],
            [{"id": "N000", "author": "Ada", "message": "Zero ID"}],
            [{"id": "N001", "author": "Ada", "message": "First"},
             {"id": "N001", "author": "Bob", "message": "Duplicate"}],
        )
        for notes in malformed:
            with self.subTest(notes=notes):
                self.ticket["notes"] = copy.deepcopy(notes)
                before = copy.deepcopy(self.tickets)
                with self.assertRaises(ValueError):
                    add_note(self.tickets, self.ticket["id"], "Bob", "Update")
                self.assertEqual(self.tickets, before)

    def test_note_ids_continue_after_existing_saved_notes(self):
        self.ticket["notes"] = [{"id": "N004", "author": "Ada", "message": "Previous"}]
        note = add_note(self.tickets, self.ticket["id"], "Bob", "New")
        self.assertEqual(note["id"], "N005")


if __name__ == "__main__":
    unittest.main()
