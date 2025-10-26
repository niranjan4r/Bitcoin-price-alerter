import unittest
from email.mime.text import MIMEText
from unittest.mock import patch, MagicMock

from src.email_notifier import send_email  # import your function


class TestSendEmail(unittest.TestCase):

    @patch("smtplib.SMTP")
    def test_send_email_success(self, mock_smtp):
        """Test successful email sending flow."""

        email_cfg = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender": "alert@example.com",
            "password": "securepassword",
            "recipient_emails": ["user1@example.com", "user2@example.com"],
        }

        subject = "BTC Drop Alert!"
        body = "Bitcoin price has dropped below threshold!"

        mock_server_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server_instance

        send_email(email_cfg, subject, body)

        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server_instance.starttls.assert_called_once()
        mock_server_instance.login.assert_called_once_with("alert@example.com", "securepassword")
        mock_server_instance.send_message.assert_called_once()

        sent_msg = mock_server_instance.send_message.call_args[0][0]
        self.assertIsInstance(sent_msg, MIMEText)
        self.assertEqual(sent_msg["Subject"], subject)
        self.assertEqual(sent_msg["From"], email_cfg["sender"])
        self.assertEqual(sent_msg["To"], ", ".join(email_cfg["recipient_emails"]))

    @patch("smtplib.SMTP", side_effect=Exception("SMTP connection failed"))
    def test_send_email_failure(self, mock_smtp):
        """Test failure when SMTP connection fails."""
        email_cfg = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender": "alert@example.com",
            "password": "securepassword",
            "recipient_emails": ["user1@example.com"],
        }

        with self.assertRaises(Exception) as context:
            send_email(email_cfg, "Test Subject", "Test Body")

        self.assertIn("SMTP connection failed", str(context.exception))


if __name__ == "__main__":
    unittest.main()
