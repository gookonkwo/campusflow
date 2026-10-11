import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'tickets.json'
        self.tickets = []
        create_ticket(self.tickets, 'Wi-Fi down', 'Network', 'high', 10)

    def test_missing_file(self):
        self.assertEqual(load_tickets(self.path), [])

    def test_restart_preserves_id_sequence(self):
        save_tickets(self.tickets, self.path)
        loaded = load_tickets(self.path)
        self.assertEqual(loaded, self.tickets)
        self.assertEqual(create_ticket(loaded, 'Printer', 'Hardware', 'low', 1)['id'], 'T002')

    def test_bad_json_preserved(self):
        self.path.write_text('{broken', encoding='utf-8')
        with self.assertRaises(ValueError):
            load_tickets(self.path)
        self.assertEqual(self.path.read_text(), '{broken')

    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):
            save_tickets(self.tickets * 2, self.path)
        self.assertFalse(self.path.exists())

    def test_invalid_schema_rejected(self):
        for field, value in [('urgency', []), ('affected_users', True),
                             ('priority', 'low'), ('status', 'unknown'),
                             ('assigned_to', ''), ('category', {}), ('id', 'T000')]:
            with self.subTest(field=field):
                ticket = dict(self.tickets[0], **{field: value})
                self.path.write_text(json.dumps([ticket]), encoding='utf-8')
                with self.assertRaises(ValueError):
                    load_tickets(self.path)

    def test_failed_replace_preserves_previous_file(self):
        save_tickets(self.tickets, self.path)
        original = self.path.read_bytes()
        create_ticket(self.tickets, 'Printer', 'Hardware', 'low', 1)
        with patch('campusflow.storage.os.replace', side_effect=OSError('Disk error')):
            with self.assertRaises(OSError):
                save_tickets(self.tickets, self.path)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])
