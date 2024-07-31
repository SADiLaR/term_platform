from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    AccountActivationTokenGenerator class is a subclass of PasswordResetTokenGenerator.

    Methods:

    _make_hash_value(self, user, timestamp):
        This method takes in a user object and a timestamp and returns a hash value
        that is used to generate an account activation token. The hash value is
        calculated by concatenating the user's primary key, timestamp, and active
        status.

        DO NOT MODIFY THIS METHOD, UNLESS YOU GET PERMISSION FROM THE PROJECT OWNER.

    """

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"


account_activation_token = AccountActivationTokenGenerator()
