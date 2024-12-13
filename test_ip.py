import unittest
from unittest.mock import patch, MagicMock
import requests  # Import requests to use exceptions like RequestException
from IPShowGUI import fetch_ip_info
from io import StringIO
from unittest.mock import patch

class TestApp(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_ip_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "ip": "123.123.123.123",
            "city": "Test City",
            "region": "Test Region",
            "country": "Test Country",
            "loc": "12.34,-56.78",
            "org": "Test ISP",
            "timezone": "UTC",
            "postal": "12345"
        }
        mock_get.return_value = mock_response

        ip_info = fetch_ip_info()
        self.assertEqual(ip_info['ip'], "123.123.123.123")
        self.assertEqual(ip_info['city'], "Test City")

    @patch('requests.get')
    def test_fetch_ip_info_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Error")
        mock_get.return_value = mock_response

        # Suppress print output during this test
        with patch('sys.stdout', new_callable=StringIO):
            ip_info = fetch_ip_info()
        self.assertIsNone(ip_info)

    @patch('requests.get')
    def test_fetch_ip_info_missing_fields(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "ip": "123.123.123.123",
            "region": "Test Region"  # Missing some fields
        }
        mock_get.return_value = mock_response

        ip_info = fetch_ip_info()
        self.assertEqual(ip_info['ip'], "123.123.123.123")
        self.assertEqual(ip_info['region'], "Test Region")
        self.assertIsNone(ip_info.get('city'))

if __name__ == "__main__":
    unittest.main()