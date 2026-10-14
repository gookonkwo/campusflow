import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from main import run
from campusflow.storage import load_tickets


class CLITests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'tickets.json'

    def play(self, answers):
        output = io.StringIO()
        with patch('builtins.input', side_effect=answers), patch('sys.stdout', output):
            result = run(self.path)
        self.assertEqual(result, 0)
        return output.getvalue()

    def test_full_workflow_and_restart(self):
        output = self.play(['1', 'Wi-Fi', 'Network', 'high', '12',
                            '2', '3', 'T001', '4', 'T001', 'Ada',
                            '5', 'T001', 'in_progress', '5', 'T001', 'resolved',
                            '5', 'T001', 'open', '6', '7', '8'])
        self.assertIn('Total tickets: 1', output)
        self.assertEqual(load_tickets(self.path)[0]['status'], 'open')
        self.play(['1', 'Printer', 'Hardware', 'low', '1', '8'])
        self.assertEqual(load_tickets(self.path)[1]['id'], 'T002')

    def test_invalid_input_then_recovery(self):
        output = self.play(['99', '1', 'Wi-Fi', 'Network', 'high', 'bad',
                            '1', 'Wi-Fi', 'Network', 'high', '12',
                            '5', 'T001', 'resolved', '8'])
        self.assertIn('Error:', output)
        self.assertEqual(len(load_tickets(self.path)), 1)
        self.assertEqual(load_tickets(self.path)[0]['status'], 'open')

    def test_save_failure_does_not_change_memory(self):
        with patch('main.save_tickets', side_effect=OSError('Disk error')):
            output = self.play(['1', 'Wi-Fi', 'Network', 'high', '12', '2', '8'])
        self.assertIn('No tickets found.', output)
        self.assertFalse(self.path.exists())

    def test_corrupt_startup_is_error(self):
        self.path.write_text('{broken')
        with patch('sys.stderr', io.StringIO()):
            self.assertEqual(run(self.path), 1)
        self.assertEqual(self.path.read_text(), '{broken')
