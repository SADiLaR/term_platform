import logging
import os
import sys

from django.test import TestCase


class LoggingTest(TestCase):
    def setUp(self):
        LOGGING_FOLDER_DEFAULT = os.path.abspath(os.path.join("/logging/"))
        self.logger = logging.getLogger("django")
        self.log_file = os.path.join(LOGGING_FOLDER_DEFAULT, "debug.log")

    def test_log_file_created(self):
        """Test if the log file is created."""
        self.logger.error("This is a test error message.")

        self.assertTrue(os.path.exists(self.log_file))

    def test_log_message(self):
        """Test if the log message is written to the file."""
        with open(self.log_file, "r") as f:
            content = f.read()
        self.assertIn("This is a test error message.", content)
