import grin


# The types module contains all the possible Grin types: GrinFloats, GrinStrings,
# and GrinInts. Each type is organized by a separate class that contains methods
# that handle the interactions between Grin types, including addition, subtraction,
# multiplication and division. Grin has a slightly different implementation than
# python and this module handles these slight changes. There also exists other classes
# for GrinTypes that have a specific meaning in the Grin language, such as Return,
# Label, and End statements.

class GrinZeroDivisionError(Exception):
    def __init__(self, error = None):
        self._error = error
        self._message = self._create_message()

    def __str__(self):
        return f'GrinZeroDivisionError: {self._message}'

    def _create_message(self) -> None:
        """Replaces python terms for grin terms in the error message"""
        message = str(self._error)
        while 'integer' in message:
            return message[:message.index('integer')] + 'GrinInt' + message[
                                                                message.index('integer') + 7:]
        while 'float' in message:
            return message[:message.index('float')] + 'GrinFloat' + message[
                                                                    message.index('float') + 5:]

class GrinType:

    def __init__(self, name = None, value = None):
        self._name = name
        self._value = value
    def add(self, value: "GrinVal") -> None:
        """Adds another value to the current value"""
        self._value += value.value()
    def subtract(self, value: "GrinVal") -> None:
        """Subtracts another value from the current value"""
        self._value -= value.value()

    def multiply(self, value: "GrinVal") -> None:
        """Multiplies another value by the current value"""
        self._value *= value.value()
    def divide(self, value: "GrinVal") -> None:
        """Divides another value by the current value"""
        self._check_for_division_of_string(self._value, value)
        try:
            if isinstance(self, GrinVar):
                self._var_divide(value)
            elif isinstance(self, GrinInt):
                self._int_divide(value)
            elif isinstance(self, GrinFloat):
                self._float_divide(value)
        except ZeroDivisionError as error:
            raise GrinZeroDivisionError(error)



    def _var_divide(self, value: "GrinVal") -> None:
        """This method divides another value by the current var and adjusts
        for the differences between python and grin"""
        if isinstance(value, GrinInt):
            if isinstance(self._value, GrinInt):
                self._value = grin_object_from_value(self._value.value() // value.value())
            elif isinstance(self._value, GrinFloat):
                self._value = grin_object_from_value(self._value.value() / value.value())
            else:
                self._check_for_division_of_string(self._value, value)


        elif isinstance(value, GrinFloat):
            if isinstance(self._value, GrinInt):
                self._value = grin_object_from_value(self._value.value() / value.value())
            elif isinstance(self._value, GrinFloat):
                self._value = grin_object_from_value(self._value.value() // value.value())
            else:
                self._check_for_division_of_string(self._value, value)

    def _int_divide(self, value: "GrinVal") -> None:
        """This method divides a GrinInt by other values, adjusting for the
        slight changes between python and grin"""
        if isinstance(value, GrinInt):
            self._value = self._value // value.value()
        elif isinstance(value, GrinFloat):
            self._value = self._value / value.value()
        else:
            self._check_for_division_of_string(self._value, value)

    def _float_divide(self, value: "GrinVal") -> None:
        """This method divides a GrinFloat by another value, not needing
        to adjust for changes because grin and python handle floats similarly"""
        self._check_for_division_of_string(self._value, value)
        self._value = self._value / value.value()

    def _check_for_division_of_string(self, value_one: "GrinVal", value_two: "GrinVal") -> None | Exception:
        if isinstance(value_one, GrinString) or isinstance(value_two, GrinString):
            raise grin.GrinTypeError(message = "GrinStrings can neither be quotient nor divisor")




class GrinVar(GrinType):
    """A GrinVar is a type that consists of a name or a value, in which the value can be of type
    GrinInt, GrinString, GrinFloat, or even GrinVar. Because the implementation of the add, subtract,
    multiply method is slightly different for GrinVars than other types, this derived class must
    override the parent class for those operations."""
    def __init__(self, name: str, value: str | int | float):
        self._name = name
        self._value = grin_object_from_value(value)

    def name(self) -> str:
        return self._name

    def value(self) -> "GrinVal":
        return self._value.value()

    def add(self, value: "GrinVal") -> None:
        self._value = grin_object_from_value(self._value.value() + value.value())

    def subtract(self, value: "GrinVal") -> None:
        self._value = grin_object_from_value(self._value.value() - value.value())

    def multiply(self, value: "GrinVal") -> None:
        try:
            self._value = grin_object_from_value(self._value.value() * value.value())
        except TypeError as error:
            raise grin.GrinTypeError(error)




class GrinInt(GrinType):
    """The GrinInt type is one that deals with integers implemented under the grin protocol"""
    def __init__(self, value: "GrinVal"):
        self._value = int(value)

    def value(self) -> int:
        return self._value

class GrinString(GrinType):
    """The GrinString type refers to strings implemented under the grin protocol"""
    def __init__(self, value: "GrinVal"):
        self._value = str(value)


    def value(self) -> str:
        return self._value


class GrinFloat(GrinType):
    """The GrinFloat type refers to numbers that are treated as floats under the grin protocol"""
    def __init__(self, value: "GrinVal"):
        self._value = float(value)

    def value(self) -> float:
        return self._value

class GrinReturn:
    pass

class GrinEnd:
    pass

class GrinLabel:
    def __init__(self, name: str, line: int):
        self._name = name
        self._line = int(line) - 1

    def name(self) -> str:
        return self._name

    def line(self) -> int:
        return self._line
def grin_object_from_value(value: str | float | int):
    if type(value) == str:
        return GrinString(value)
    elif type(value) == int:
        return GrinInt(value)
    elif type(value) == float:
        return GrinFloat(value)


__all__ = [
    grin_object_from_value.__name__,
    GrinLabel.__name__,
    GrinEnd.__name__,
    GrinReturn.__name__,
    GrinFloat.__name__,
    GrinString.__name__,
    GrinInt.__name__,
    GrinVar.__name__,
    GrinType.__name__,
    GrinZeroDivisionError.__name__,
]