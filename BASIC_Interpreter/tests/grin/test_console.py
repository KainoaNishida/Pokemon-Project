import unittest

from grin import GrinParseError
from grin.console import *


class TestConsole(unittest.TestCase):
    def setUp(self) -> None:
        self.empty_code = ['.']
        self.valid_code = ['LET A 3', '.']
        self.invalid_line = ['-abc']
        self.invalid_code = ['GOTO 3 IF 4 < 5 "Boo"']
        self.interface = Interface()

    def test_parsing_empty_code_returns_empty_generator(self):
        with self.assertRaises(StopIteration):
            parsed_code = self.interface._parse_input(self.empty_code)
            parsed_code.__next__()

    def test_parsing_valid_lines_returns_generator_with_code(self):
        parsed_code = self.interface._parse_input(self.valid_code)
        self.assertEqual([x.value() for x in parsed_code.__next__()], ['LET', 'A', 3])

    def test_parsing_invalid_code_raises_parsing_error(self):
        with self.assertRaises(GrinParseError):
            parsed_code = self.interface._parse_input(self.invalid_code)
            parsed_code.__next__()

if __name__ == '__main__':
    unittest.main()


