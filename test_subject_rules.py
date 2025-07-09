import unittest
from process_emails import match_rule

class TestMatchRule(unittest.TestCase):
    def setUp(self):
        self.email = {
            'subject': 'Test Subject',
            'body': 'This is a test email body.',
            'sender': 'test@example.com',
            'received_at': '2024-06-01T12:00:00'
        }

    def test_equals_predicate_true(self):
        rule = {'field': 'subject', 'predicate': 'equals', 'value': 'Test Subject'}
        self.assertTrue(match_rule(self.email, rule))

    def test_equals_predicate_false(self):
        rule = {'field': 'subject', 'predicate': 'equals', 'value': 'Another Subject'}
        self.assertFalse(match_rule(self.email, rule))

    def test_does_not_equal_predicate_true(self):
        rule = {'field': 'subject', 'predicate': 'does not equal', 'value': 'Another Subject'}
        self.assertTrue(match_rule(self.email, rule))

    def test_does_not_equal_predicate_false(self):
        rule = {'field': 'subject', 'predicate': 'does not equal', 'value': 'Test Subject'}
        self.assertFalse(match_rule(self.email, rule))

if __name__ == '__main__':
    unittest.main()