import unittest

from grin.comparisons import *
import grin.types
from grin.types import *



class TestComparisons(unittest.TestCase):
    def setUp(self):
        self._gi = grin.types.GrinInt(1)
        self._gf = grin.types.GrinFloat(1.0)
        self._gs = grin.types.GrinString('abc')
        self._eq_statement = self._create_equal_token_sequence()
        self._ne_statement = self._create_unequal_token_sequence()
        self._gt_statement = self._create_greater_than_token_sequence()
        self._ge_statement = self._create_greater_than_or_equal_to_token_sequence()
        self._lt_statement = self._create_less_than_token_sequence()
        self._le_statement = self._create_less_than_or_equal_to_token_sequence()
        self._error_invalid_conditional = self._create_error_invalid_conditional()


    def test_two_equal_values__equal_is_true(self):
        equal_obj = Equal(self._gi, self._gf)
        self.assertTrue(equal_obj.test())

    def test_two_equal_values__unequal_is_false(self):
        not_equal_obj = NotEqual(self._gi, self._gf)
        self.assertFalse(not_equal_obj.test())

    def test_two_equal_values__greater_than_is_false(self):
        greater_than_obj = GreaterThan(self._gi, self._gf)
        self.assertFalse(greater_than_obj.test())

    def test_two_equal_values__greater_than_or_equal_to_is_true(self):
        greater_than_or_equal_to_obj = GreaterThanOrEqual(self._gi, self._gf)
        self.assertTrue(greater_than_or_equal_to_obj.test())

    def test_two_equal_values__less_than_is_false(self):
        less_than_obj = LessThan(self._gi, self._gf)
        self.assertFalse(less_than_obj.test())

    def test_two_equal_values__less_than_or_equal_to_is_true(self):
        less_than_or_equal_to_obj = LessThanOrEqual(self._gi, self._gf)
        self.assertTrue(less_than_or_equal_to_obj.test())

    def test_changing_first_value_of_comparison(self):
        comparison = Comparison(GrinInt(1), GrinInt(2))
        comparison.change_first_value(GrinInt(3))
        self.assertEqual(comparison.first_value().value(), 3)

    def test_create_equal_statement__returns_correct_statement(self):
        grin_comparison = create_comparison(self._eq_statement)
        self.assertEqual(type(grin_comparison), Equal)

    def test_create_unequal_statement__returns_unequal_statement(self):
        grin_comparison = create_comparison(self._ne_statement)
        self.assertEqual(type(grin_comparison), NotEqual)

    def test_create_greater_than_statement__returns_unequal_statement(self):
        grin_comparison = create_comparison(self._gt_statement)
        self.assertEqual(type(grin_comparison), GreaterThan)

    def test_create_greater_than_or_equal_statement__returns_unequal_statement(self):
        grin_comparison = create_comparison(self._ge_statement)
        self.assertEqual(type(grin_comparison), GreaterThanOrEqual)

    def test_create_less_than_statement__returns_unequal_statement(self):
        grin_comparison = create_comparison(self._lt_statement)
        self.assertEqual(type(grin_comparison), LessThan)

    def test_create_less_than_or_equal_statement__returns_unequal_statement(self):
        grin_comparison = create_comparison(self._le_statement)
        self.assertEqual(type(grin_comparison), LessThanOrEqual)

    def test_error_conditional_initialized(self):
        with self.assertRaises(GrinComparisonError):
            create_comparison(self._error_invalid_conditional)

    def test_error_conditional_has_correct_string(self):
        try:
            create_comparison(self._error_invalid_conditional)
        except GrinComparisonError as error:
            self.assertEqual(str(error), "GrinComparisonError: Go statement followed by an invalid statement; not a conditional")

    def test_comparing_unequal_string_to_float_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2 <> "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" <> 2', 1)])
            test.test()

    def test_comparing_unequal_string_to_int_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2.0 <> "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" <> 2.0', 1)])
            test.test()

    def test_comparing_equal_string_to_int_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2 = "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" = 2', 1)])
            test.test()

    def test_comparing_equal_string_to_float_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2.0 = "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" = 2.0', 1)])
            test.test()

    def test_comparing_greater_than_string_to_int_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2 > "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" > 2', 1)])
            test.test()

    def test_comparing_greater_than_string_to_float_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2.0 > "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" > 2.0', 1)])
            test.test()

    def test_comparing_greater_than_or_equal_string_to_int_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2 >= "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" >= 2', 1)])
            test.test()

    def test_comparing_greater_than_or_equal_string_to_float_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2.0 >= "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" >= 2.0', 1)])
            test.test()

    def test_comparing_less_than_string_to_int_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2 < "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" < 2', 1)])
            test.test()

    def test_comparing_less_than_string_to_float_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2.0 < "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" < 2.0', 1)])
            test.test()

    def test_comparing_less_than_or_equal_string_to_int_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2 <= "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" <= 2', 1)])
            test.test()

    def test_comparing_less_than_or_equal_string_to_float_raises_error(self):
        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2.0 <= "HI"', 1)])
            test.test()

        with self.assertRaises(grin.statements.GrinTypeError):
            test = create_comparison([x for x in grin.lexing.to_tokens('IF "HI" <= 2.0', 1)])
            test.test()

    def test_comparing_string_to_nonstring_raises_error_with_correct_message(self):
        try:
            test = create_comparison([x for x in grin.lexing.to_tokens('IF 2 <> "HI"', 1)])
            test.test()
        except grin.statements.GrinTypeError as error:
            self.assertEqual(str(error), "GrinTypeError: type GrinString cannot be compared to type other than GrinString")

    def test_comparison_float_and_string_raises_error_with_correct_message(self):
        try:
            1 < "error"
        except TypeError as error:
            grin_error = GrinComparisonError(error)
            self.assertEqual(str(grin_error), "GrinComparisonError: '<' not supported between instances of 'GrinInt' and 'GrinString'")

    def test_comparison_int_and_string_raises_error_with_correct_message(self):
        try:
            1.0 < "error"
        except TypeError as error:
            grin_error = GrinComparisonError(error)
            self.assertEqual(str(grin_error),
                             "GrinComparisonError: '<' not supported between instances of 'GrinFloat' and 'GrinString'")


    def _create_equal_token_sequence(self):
        return [x for x in grin.lexing.to_tokens("IF 1 = 1", 1)]

    def _create_unequal_token_sequence(self):
        return [x for x in grin.lexing.to_tokens("IF 1 <> 1", 1)]

    def _create_greater_than_token_sequence(self):
        return [x for x in grin.lexing.to_tokens("IF 1 > 1", 1)]

    def _create_greater_than_or_equal_to_token_sequence(self):
        return [x for x in grin.lexing.to_tokens("IF 1 >= 1", 1)]

    def _create_less_than_token_sequence(self):
        return [x for x in grin.lexing.to_tokens("IF 1 < 1", 1)]

    def _create_less_than_or_equal_to_token_sequence(self):
        return [x for x in grin.lexing.to_tokens("IF 1 <= 1", 1)]

    def _create_error_invalid_conditional(self):
        return [x for x in grin.lexing.to_tokens("HI", 1)]






if __name__ == '__main__':
    unittest.main()
