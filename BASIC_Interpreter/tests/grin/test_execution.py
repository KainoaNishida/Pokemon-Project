import unittest

from grin import Interface, Conversion
from grin.execution import *
import grin

# Since this module implements all other modules, it is very difficult to test. However,
# lines of the execution module are nevertheless tested as a byproduct of unittests for the
# other modules, as this module leaves all features and implementations of the other modules
# intact. We can still test its basic methods, such as the methods that allow access to the
# information within an execution object.

class TestExecution(unittest.TestCase):
    def setUp(self) -> None:
        self._execution = Execution(self._create_conversion_object())

    def test_execution_object_returns_index(self):
        self.assertEqual(self._execution.index(), 1)

    def test_initialized_execution_object_returns_empty_dict_of_labels(self):
        self.assertEqual(list(self._execution.labels().keys()), ['ABC'])

    def test_initialized_execution_object_returns_empty_dict_of_variables(self):
        self.assertEqual(list(self._execution.vars().keys()), ['VAR'])

    def test_execution_object_returns_grin_code(self):
        self.assertEqual([type(x) for x in self._execution.grin_code()], [grin.statements.Print, grin.types.GrinEnd])

    def test_execution_object_returns_true_gosub_if_not_initalized_as_false(self):
        self.assertTrue(self._execution.gosub_status())

    def test_execution_object_returns_false_gosub_turned_off(self):
        self._execution.turn_off_gosub()
        self.assertFalse(self._execution.gosub_status())

    def test_execution_object_returns_true_gosub_turned_on(self):
        self._execution.turn_on_gosub()
        self.assertTrue(self._execution.gosub_status())
    def _create_conversion_object(self):
        interface = Interface()
        self._parsed_code = interface._parse_input(["ABC: PRINT VAR", "END"])
        conversion_obj = Conversion(self._parsed_code)
        conversion_obj.convert()
        return conversion_obj

if __name__ == '__main__':
    unittest.main()