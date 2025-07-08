import unittest
from process_emails import match_rule
from datetime import datetime, timedelta

class TestRuleMatching(unittest.TestCase):
    def test_subject_contains(self):
        email = {'subject': 'Hello world'}
        rule = {'field': 'Subject', 'predicate': 'Contains', 'value': 'hello'}
        self.assertTrue(match_rule(email, rule))

    def test_subject_does_not_contain(self):
        email = {'subject': 'Hello world'}
        rule = {'field': 'Subject', 'predicate': 'Does not Contain', 'value': 'spam'}
        self.assertTrue(match_rule(email, rule))

    def test_received_date_less_than(self):
        email = {'received_at': (datetime.now() - timedelta(days=2)).isoformat()}
        rule = {'field': 'Received_at', 'predicate': 'Less than', 'value': '3'}
        self.assertTrue(match_rule(email, rule))

    def test_received_date_greater_than(self):
        email = {'received_at': (datetime.now() - timedelta(days=5)).isoformat()}
        rule = {'field': 'Received_at', 'predicate': 'Greater than', 'value': '3'}
        self.assertTrue(match_rule(email, rule))

if __name__ == '__main__':
    unittest.main()
