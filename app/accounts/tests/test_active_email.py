from unittest.mock import MagicMock, patch

from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.test import RequestFactory, TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.service.active_email import (  # Adjust the import path as necessary
    SendActiveEmailService,
)
from accounts.tokens import account_activation_token
from users.models import CustomUser  # Import your custom user model


class SendActiveEmailServiceTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.request = self.factory.get("/fake-path")
        self.service = SendActiveEmailService()

    def test_send_activation_email(self):
        with patch("accounts.service.active_email.render_to_string") as mock_render:
            # Set up the mocks
            mock_render.return_value = "<html>mocked template</html>"

            # # Call the method
            self.service.send_activation_email(self.request, self.user)

            # Check that render_to_string was called with the correct parameters
            mock_render.assert_called_once_with(
                "accounts/email/activation_email.html",
                {
                    "user": self.user,
                    "domain": get_current_site(self.request).domain,
                    "uid": urlsafe_base64_encode(force_bytes(self.user.pk)),
                    "token": account_activation_token.make_token(self.user),
                },
            )

            # Check that an email was sent
            self.assertEqual(len(mail.outbox), 1)
            sent_email = mail.outbox[0]
            self.assertEqual(sent_email.subject, "Activate your account.")
            self.assertEqual(sent_email.to, [self.user.email])
            self.assertIn("mocked template", sent_email.alternatives[0][0])
            self.assertEqual(sent_email.alternatives[0][1], "text/html")
            self.assertIn(
                "Please activate your account by clicking the link provided in the email.",
                sent_email.body,
            )
