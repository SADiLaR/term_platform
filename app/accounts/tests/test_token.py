import unittest
from datetime import datetime

from accounts.tokens import AccountActivationTokenGenerator


# Speculate user model class for test abstraction
class User:
    def __init__(self, id, is_active):
        self.pk = id
        self.is_active = is_active


class TestAccountActivationTokenGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = AccountActivationTokenGenerator()
        self.timestamp = datetime.now()

    def test_make_hash_value_active_user(self):
        user = User(1, True)
        hash_val = self.generator._make_hash_value(user, self.timestamp)
        expected_val = f"{user.pk}{self.timestamp}{user.is_active}"
        self.assertEqual(hash_val, expected_val)

    def test_make_hash_value_inactive_user(self):
        user = User(1, False)
        hash_val = self.generator._make_hash_value(user, self.timestamp)
        expected_val = f"{user.pk}{self.timestamp}{user.is_active}"
        self.assertEqual(hash_val, expected_val)


if __name__ == "__main__":
    unittest.main()
