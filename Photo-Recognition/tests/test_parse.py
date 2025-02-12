import unittest
from unittest.mock import patch
from main import parse_response

# FILE: tests/test_main.py

class TestParseResponse(unittest.TestCase):
    def test_parse_response(self):
        response_text = "apple: 5\nbanana: 3\norange: 2"
        expected_output = {
            "apple": 5,
            "banana": 3,
            "orange": 2
        }
        self.assertEqual(parse_response(response_text), expected_output)

    def test_parse_response_with_extra_spaces(self):
        response_text = "  apple  :  5  \n  banana:3\norange:  2  "
        expected_output = {
            "apple": 5,
            "banana": 3,
            "orange": 2
        }
        self.assertEqual(parse_response(response_text), expected_output)

    def test_parse_response_with_invalid_format(self):
        response_text = "apple 5\nbanana: 3\norange: 2"
        expected_output = {
            "banana": 3,
            "orange": 2
        }
        self.assertEqual(parse_response(response_text), expected_output)

if __name__ == '__main__':
    with patch.dict('sys.modules', {'network': None, 'urequests': None}):
        unittest.main()