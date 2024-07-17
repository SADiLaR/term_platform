from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import account_activation_token


class SendActiveEmailService:
    @staticmethod
    def send_activation_email(request, user):
        if user and request:
            current_site = get_current_site(request)
            mail_subject = "Activate your account."
            message = render_to_string(
                "accounts/email/activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            text_content = (
                "Please activate your account by clicking the link provided in the email."
            )
            email = EmailMultiAlternatives(
                mail_subject, text_content, "your-email@example.com", [user.email]
            )
            email.attach_alternative(message, "text/html")
            email.send()
