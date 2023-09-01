import unittest

from grin.statements import *
from grin.types import GrinVar, GrinInt, GrinFloat, GrinString


class TestStatements(unittest.TestCase):
    def setUp(self):
        self._grin_var = GrinVar('a', 3)
        self._grin_int = GrinInt(3)
        self._innum_test_obj = Innum('test')
        self._instr_test_obj = Instr('test')
    def test_let_statement_returns_correct_type(self):
        self._let_statement = Let('A', 3)
        self.assertTrue(isinstance(self._let_statement.test(), GrinVar))

    def test_add_statement_correctly_adds_integer(self):
        testcase = Add(GrinInt(5), GrinInt(5))
        self.assertEqual(testcase.test().value(), 10)

    def test_subtract_int_from_float_yields_float(self):
        testcase = Sub(self._grin_var, GrinFloat(4.0))
        self.assertEqual(testcase.test().value(), -1.0)

    def test_multiply_int_by_int_yields_int(self):
        testcase = Mult(self._grin_var, GrinInt(3))
        self.assertEqual(testcase.test().value(), 9)

    def test_multiply_int_by_float_yields_float(self):
        testcase = Mult(self._grin_var, GrinFloat(3.0))
        self.assertEqual(testcase.test().value(), 9.0)

    def test_divide_int_by_int_yields_int(self):
        testcase = Div(self._grin_var, GrinInt(3))
        self.assertEqual(testcase.test().value(), 1)

    def test_divide_int_by_float_yields_float(self):
        testcase = Div(self._grin_var, GrinFloat(3.0))
        self.assertEqual(testcase.test().value(), 1.0)

    def test_print_int_correctly_prints_its_value(self):
        testcase = Print(self._grin_var)
        self.assertEqual(str(testcase.test()), '3')

    def test_add_between_int_and_string_creates_correct_exception(self):
        error = Add(GrinInt(3), GrinString("test"))
        with self.assertRaises(GrinTypeError):
            error.test()

    def test_exception_while_adding_int_and_string_creates_correct_message(self):
        testcase = Add(GrinInt(3), GrinString("test"))
        try:
            testcase.test()
        except GrinTypeError as error:
            self.assertEqual(str(error), "GrinTypeError: unsupported operand type(s) for +=: 'GrinInt' and 'GrinString'")

    def test_exception_while_adding_float_and_int_creates_correct_message(self):
        testcase = Add(GrinFloat(3.0), GrinString("test"))
        try:
            testcase.test()
        except GrinTypeError as error:
            self.assertEqual(str(error), "GrinTypeError: unsupported operand type(s) for +=: 'GrinFloat' and 'GrinString'")

    def test_instr_creates_variable_with_string_value(self):
        var = self._instr_test_obj.test('value')
        self.assertEqual("value", var.value())

    def test_innum_can_create_variable_with_int_value(self):
        var = self._innum_test_obj.test('1')
        self.assertEqual(1, var.value())

    def test_innum_can_create_variable_with_float_value(self):
        var = self._innum_test_obj.test('1.0')
        self.assertEqual(1.0, var.value())

    def test_innum_raises_error_when_input_is_neither_int_nor_float(self):
        with self.assertRaises(GrinValueError):
            self._innum_test_obj.test('error')

    def test_grin_type_error_contains_message_when_initialized(self):
        error = GrinTypeError(message = 'error')
        self.assertEqual(str(error), 'GrinTypeError: error')

    def test_grin_value_error_contains_message_when_initialized(self):
        error = GrinValueError(message = 'error')
        self.assertEqual(str(error), 'GrinValueError: error')

    def test_grin_type_error_creates_message_replaces_int_with_grinint(self):
        try:
            1 + 'cannot add string by int'
        except TypeError as error:
            self.assertTrue("GrinInt" in str(GrinTypeError(error)))

    def test_grin_type_error_creates_message_replaces_float_with_grinfloat(self):
        try:
            1.0 + 'cannot add string by int'
        except TypeError as error:
            self.assertTrue('GrinFloat' in str(GrinTypeError(error)))

    def test_grin_value_error_creates_message_replaces_int_with_grinint(self):
        try:
            int("hello")
        except ValueError as error:
            self.assertTrue('GrinInt' in str(GrinValueError(error)))

    def test_grin_value_error_creates_message_replaces_float_with_grinfloat(self):
        try:
            float("hello")
        except ValueError as error:
            self.assertTrue('GrinFloat' in str(GrinValueError(error)))

    def test_grin_go_error_has_correct_message(self):
        error = GrinGoError('error')
        self.assertEqual(str(error), 'GrinGoError: error')

    def test_print_statement_contains_event(self):
        print_test = Print(1)
        print_test._tv = print_test._value
        print_test._create_statement()
        self.assertEqual((print_test.event()), '1')

    def test_innum_handles_exceptions_in_input_with_underscore(self):
        innum_test = Innum('test')
        with self.assertRaises(GrinValueError):
            innum_test._float_or_int('_')

    def test_innum_handles_exceptions_in_input_with_comma(self):
        innum_test = Innum('test')
        with self.assertRaises(GrinValueError):
            innum_test._float_or_int(',')

    def test_go_object_can_check_if_zero_when_true(self):
        go_test = Go(None, None)
        self.assertTrue(go_test._check_if_zero(1))

    def test_go_object_can_raise_error_if_check_is_zero_is_false(self):
        go_test = Go(None, None)
        with self.assertRaises(GrinGoError):
            go_test._check_if_zero(0)

    def test_go_object_raises_grin_go_error_if_target_is_float(self):
        go_test = Go(None, None)
        with self.assertRaises(GrinTypeError):
            go_test._check_float_error(1.0)

    def test_go_object_exception_not_raised_if_target_is_nonzero_int(self):
        go_test = Go(None, None)
        go_test._check_float_error(1)


if __name__ == '__main__':
    unittest.main()
