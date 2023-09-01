
import grin
from grin.types import *

# The comparisons module organizes all types of comparisons, which are commonly present in grin
# conditionals that follow Go statements. All evaluations and types of exceptions that can be raised during the
# process of evaluating a grin conditional are handled here.

class GrinComparisonError(Exception):
    """The GrinComparisonError is an exception raised when there was an issue constructing a
    conditional."""
    def __init__(self, error: Exception):
        self._error = error
        self._message = self._create_message()


    def __str__(self):
        return f'GrinComparisonError: {self._message}'

    def _create_message(self) -> None:
        """Replaces python terms for grin terms in the error message"""
        message = str(self._error)
        while 'int' in message:
            message = message[:message.index('int')] + 'GrinInt' + message[
                                                                   message.index('int') + 3:]
        while 'str' in message:
            message = message[:message.index('str')] + 'GrinString' + message[
                                                                      message.index('str') + 3:]
        while 'float' in message:
            message = message[:message.index('float')] + 'GrinFloat' + message[
                                                                       message.index('float') + 5:]
        return message


class Comparison:
    """The comparison class is a superclass that contains underlying methods and information
    between all derived classes that inherit from it. One such necessary method that is shared
    by all child classes is the is_true() method, which evaluates to truthy or falsy for a
    specific instance of a comparison object (Equal, Unequal, etc.) and its two values."""
    def __init__(self, first_value, second_value):
        self._first_value = first_value
        self._second_value = second_value

    def change_first_value(self, value: "GrinVal") -> None:
        self._first_value = value

    def first_value(self) -> "GrinVal":
        return self._first_value

    def is_true(self, statement: "comparison", execution: "Execution") -> bool | Exception:
        try:
            return self._conditional_from_object(statement, execution)
        except TypeError as error:
            if isinstance(error, grin.GrinTypeError):
                raise error
            else:
                raise GrinComparisonError(error)

    def _conditional_from_object(self, statement: "comparison", execution = None) -> bool:
        if self._first_value.value() in execution.vars().keys():
            while self._first_value.value() in execution.vars().keys():
                self._first_value = execution.vars()[self._first_value.value()]
        if self._second_value.value() in execution.vars().keys():
            while self._second_value.value() in execution.vars().keys():
                self._second_value = execution.vars()[self._second_value.value()]

        self._check_compatability_of_types()

        if statement is Equal:
            return self._first_value.value() == self._second_value.value()
        if statement is NotEqual:
            return self._first_value.value() != self._second_value.value()
        if statement is GreaterThan:
            return self._first_value.value() > self._second_value.value()
        if statement is GreaterThanOrEqual:
            return self._first_value.value() >= self._second_value.value()
        if statement is LessThan:
            return self._first_value.value() < self._second_value.value()
        if statement is LessThanOrEqual:
            return self._first_value.value() <= self._second_value.value()


    def _check_compatability_of_types(self) -> None | Exception:
        if isinstance(self._first_value, GrinString):
            if not isinstance(self._second_value, GrinString):
                raise grin.GrinTypeError(message = "type GrinString cannot be compared to type other than GrinString")
        if isinstance(self._second_value, GrinString):
           if not isinstance(self._first_value, GrinString):
                raise grin.GrinTypeError(message = "type GrinString cannot be compared to type other than GrinString")



class Equal(Comparison):
    """Returns true if two grin values are equal; false otherwise"""
    def is_true(self, execution) -> bool:
        return super().is_true(type(self), execution)

    def test(self):
        self._check_compatability_of_types()
        return self._first_value.value() == self._second_value.value()

class NotEqual(Comparison):
    """Returns true if two grin values are not equal; false otherwise"""
    def is_true(self, execution) -> bool:
        return super().is_true(type(self), execution)

    def test(self):
        self._check_compatability_of_types()
        return self._first_value.value() != self._second_value.value()
class GreaterThan(Comparison):
    """Returns true if the first grin value is greater than the second; false otherwise"""
    def is_true(self, execution) -> bool:
        return super().is_true(type(self), execution)

    def test(self):
        self._check_compatability_of_types()
        return self._first_value.value() > self._second_value.value()
class GreaterThanOrEqual(Comparison):
    """Returns true if the first grin value is greater than or equal to the second; false otherwise"""
    def is_true(self, execution) -> bool:
        return super().is_true(type(self), execution)

    def test(self):
        self._check_compatability_of_types()
        return self._first_value.value() >= self._second_value.value()
class LessThan(Comparison):
    """Returns true if the first value is less than the second value; false otherwise"""
    def is_true(self, execution) -> bool:
        return super().is_true(type(self), execution)

    def test(self):
        self._check_compatability_of_types()
        return self._first_value.value() < self._second_value.value()
class LessThanOrEqual(Comparison):
    """Returns true if the first value is less than or equal to the second value; false otherwise"""
    def is_true(self, execution) -> bool:
        return super().is_true(type(self), execution)

    def test(self):
        self._check_compatability_of_types()
        return self._first_value.value() <= self._second_value.value()

def create_comparison(sequence: "iterable[GrinToken]"):
    """Creates a comparison object from a sequence of grin tokens, storing information about the first
    value and the second value in the process"""
    if sequence[0].kind().index() == 12:
        if sequence[2].kind().index() == 6:
            return Equal(grin_object_from_value(sequence[1].value()),
                         grin_object_from_value(sequence[3].value()))
        elif sequence[2].kind().index() == 9:
            return GreaterThan(grin_object_from_value(sequence[1].value()),
                         grin_object_from_value(sequence[3].value()))
        elif sequence[2].kind().index() == 10:
            return GreaterThanOrEqual(grin_object_from_value(sequence[1].value()),
                         grin_object_from_value(sequence[3].value()))
        elif sequence[2].kind().index() == 15:
            return LessThan(grin_object_from_value(sequence[1].value()),
                         grin_object_from_value(sequence[3].value()))
        elif sequence[2].kind().index() == 16:
            return LessThanOrEqual(grin_object_from_value(sequence[1].value()),
                         grin_object_from_value(sequence[3].value()))
        elif sequence[2].kind().index() == 22:
            return NotEqual(grin_object_from_value(sequence[1].value()),
                         grin_object_from_value(sequence[3].value()))
    else:
        raise GrinComparisonError("Go statement followed by an invalid statement; not a conditional")


__all__ = [
    create_comparison.__name__,
    LessThanOrEqual.__name__,
    LessThan.__name__,
    GreaterThan.__name__,
    GreaterThanOrEqual.__name__,
    NotEqual.__name__,
    Equal.__name__,
    Comparison.__name__,
    GrinComparisonError.__name__,
]