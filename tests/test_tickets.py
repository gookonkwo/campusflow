import unittest
from campusflow.tickets import create_ticket, priority_for


class TicketTests(unittest.TestCase):
    def test_critical(self): self.assertEqual(priority_for('high', 12), 'critical')
    def test_high(self): self.assertEqual(priority_for('high', 2), 'high')
    def test_medium(self): self.assertEqual(priority_for('low', 4), 'medium')
    def test_low(self): self.assertEqual(priority_for('low', 1), 'low')
    def test_zero_rejected(self):
        with self.assertRaises(ValueError): create_ticket([], 'hello', 'network', 'low', 0)
    def test_blank_title_rejected(self):
        with self.assertRaises(ValueError): create_ticket([], ' ', 'network', 'low', 1)
    def test_case_normalized(self):
        ticket = create_ticket([], 'HELLO', 'nEtWoRk', 'HIGH', 11)
        self.assertEqual((ticket['category'], ticket['urgency']), ('Network', 'high'))
