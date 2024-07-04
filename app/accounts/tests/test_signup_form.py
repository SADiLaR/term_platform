import unittest

from django.test import TestCase

from accounts.forms import CustomUserCreationForm


class CustomUserCreationFormTest(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.email = "testuser@gmail.com"
        self.first_name = "Test"
        self.last_name = "User"
        self.password1 = "sadilar2024"
        self.password2 = "sadilar2024"

    def test_valid_data(self):
        form = CustomUserCreationForm(
            {
                "username": self.username,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password1": self.password1,
                "password2": self.password2,
            }
        )

        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = CustomUserCreationForm({})
        self.assertFalse(form.is_valid())

        self.assertEqual(
            form.errors,
            {
                "username": ["This field is required."],
                "email": ["This field is required."],
                "first_name": ["This field is required."],
                "last_name": ["This field is required."],
                "password1": ["This field is required."],
                "password2": ["This field is required."],
            },
        )

    def test_invalid_email(self):
        form = CustomUserCreationForm(
            {
                "username": self.username,
                "email": "not a valid email",
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password1": self.password1,
                "password2": self.password2,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "email": ["Enter a valid email address."],
            },
        )

    def test_passwords_do_not_match(self):
        form = CustomUserCreationForm(
            {
                "username": self.username,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password1": self.password1,
                "password2": "wrong password",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "password2": ["The two password fields didn’t match."],
            },
        )


if __name__ == "__main__":
    unittest.main()
