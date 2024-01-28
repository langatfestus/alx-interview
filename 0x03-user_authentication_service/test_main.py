import unittest
from unittest.mock import patch
from main import log_in

class TestLogIn(unittest.TestCase):

    @patch('main.requests.post')
    def test_successful_login(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"session_id": "12345"}

        result = log_in("test@example.com", "password")

        self.assertEqual(result, "12345")

    @patch('main.requests.post')
    def test_failed_login(self, mock_post):
        mock_post.return_value.status_code = 401
        mock_post.return_value.text = "Unauthorized"

        with self.assertRaises(AssertionError):
            log_in("test@example.com", "password")