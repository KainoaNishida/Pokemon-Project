import unittest

from grin.types import *
import grin

class TestTypes(unittest.TestCase):
    def setUp(self):
        self._grin_var = GrinVar('A', 3)
        self._grin_int = GrinInt(3)
        self._grin_float = GrinFloat(3.00)
        self._grin_string = GrinString('test')

    def test_grin_var_has_correct_name(self):
        self.assertEqual(self._grin_var.name(), 'A')

    def test_grin_var_has_correct_value(self):
        self.assertEqual(self._grin_var.value(), 3)

    def test_grin_int_has_correct_value(self):
        self.assertEqual(self._grin_int.value(), 3)

    def test_grin_var_add_method__yields_grin_var(self):
        tv = GrinVar('A', 3)
        tv.add(GrinInt(3))
        self.assertIsInstance(tv, GrinVar)

    def test_grin_var_add_method__grin_var_has_correct_value(self):
        tv = GrinVar('A', 3)
        tv.add(GrinInt(3))
        self.assertEqual(6, tv.value())
    def test_grin_var_subtract_method__yields_grin_var(self):
        tv = GrinVar('A', 3)
        tv.subtract(GrinInt(3))
        self.assertIsInstance(tv, GrinVar)

    def test_grin_var_subtract_method__grin_var_has_correct_value(self):
        tv = GrinVar('A', 3)
        tv.subtract(GrinInt(3))
        self.assertEqual(0, tv.value())

    def test_grin_var_multiply_method__yields_grin_var(self):
        tv = GrinVar('A', 3)
        tv.multiply(GrinInt(3))
        self.assertIsInstance(tv, GrinVar)

    def test_grin_var_multiply_method__grin_var_has_correct_value(self):
        tv = GrinVar('A', 3)
        tv.multiply(GrinInt(3))
        self.assertEqual(9, tv.value())


    def test_grin_float_has_correct_value(self):
        self.assertEqual(self._grin_float.value(), 3.00)

    def test_grin_string_has_correct_value(self):
        self.assertEqual(self._grin_string.value(), 'test')

    def test_add_int_to_int_yields_int(self):
        temp_int = GrinInt(1)
        temp_int.add(self._grin_int)
        self.assertEqual(temp_int.value(), int(4))

    def test_add_float_to_int_yields_float(self):
        temp_float = GrinInt(1.0)
        temp_float.add(self._grin_int)
        self.assertEqual(temp_float.value(), float(4))

    def test_add_float_to_float_yields_float(self):
        temp_float = GrinInt(1.0)
        temp_float.add(self._grin_float)
        self.assertEqual(temp_float.value(), float(4))

    def test_grin_label_returns_correct_name(self):
        grin_label = GrinLabel('GOSUB', 4)
        self.assertEqual('GOSUB', grin_label.name())

    def test_grin_label_returns_correct_index(self):
        grin_label = GrinLabel('GOSUB', 4)
        self.assertEqual(3, grin_label.line())

    def test_grin_object_from_value__string(self):
        self.assertIsInstance(grin_object_from_value('abc'), GrinString)

    def test_grin_object_from_value__integer(self):
        self.assertIsInstance(grin_object_from_value(1), GrinInt)

    def test_grin_object_from_value__float(self):
        self.assertIsInstance(grin_object_from_value(1.0), GrinFloat)

    def test_divide_int_by_int__correct_result(self):
        g1 = GrinInt(8)
        g2 = GrinInt(2)
        g1.divide(g2)
        self.assertEqual(g1.value(), 4)

    def test_divide_int_by_float__correct_result(self):
        g1 = GrinInt(8)
        g2 = GrinFloat(2.0)
        g1.divide(g2)
        self.assertEqual(g1.value(), 4.0)

    def test_divide_float_by_int__correct_result(self):
        g1 = GrinFloat(8)
        g2 = GrinInt(2.0)
        g1.divide(g2)
        self.assertEqual(g1.value(), 4.0)

    def test_var_divide_int_value_by_int__correct_result(self):
        g1 = self._create_grin_var_with_int_value()
        g1.divide(GrinInt(3))
        self.assertEqual(g1.value(), 1)

    def test_var_divide_float_value_by_int__correct_result(self):
        g1 = self._create_grin_var_with_float_value()
        g1.divide(GrinInt(3))
        self.assertEqual(g1.value(), 1.0)

    def test_var_divide_float_value_by_float__correct_result(self):
        g1 = self._create_grin_var_with_float_value()
        g1.divide(GrinFloat(3.0))
        self.assertEqual(g1.value(), 1.0)

    def test_division_by_int_zero_raises_error(self):
        with self.assertRaises(GrinZeroDivisionError):
            self._grin_int.divide(GrinInt(0))

    def test_division_by_int_zero_raises_error_with_correct_string(self):
        try:
            self._grin_int.divide(GrinInt(0))
        except GrinZeroDivisionError as error:
            self.assertEqual(str(error), "GrinZeroDivisionError: GrinInt division or modulo by zero")

    def test_division_by_float_zero_raises_error(self):
        with self.assertRaises(GrinZeroDivisionError):
            self._grin_int.divide(GrinFloat(0.0))

    def test_division_by_float_zero_raises_error_with_correct_string(self):
        try:
            self._grin_int.divide(GrinFloat(0.0))
        except GrinZeroDivisionError as error:
            self.assertEqual(str(error),
                             "GrinZeroDivisionError: GrinFloat division by zero")

    def test_string_as_quotient_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            GrinVar('A', 'test').divide(GrinInt(1))

    def test_string_as_divisor_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            GrinInt(1).divide(GrinString('error'))

    def test_string_division_raises_error_with_correct_string(self):
        try:
            GrinInt(1).divide(GrinString('error'))
        except grin.statements.GrinTypeError as error:
            self.assertEqual(str(error), "GrinTypeError: GrinStrings can neither be quotient nor divisor")


    def _create_grin_var_with_int_value(self):
        return GrinVar('test', 3)

    def _create_grin_var_with_float_value(self):
        return GrinVar('test', 3.0)




if __name__ == '__main__':
    unittest.main()
