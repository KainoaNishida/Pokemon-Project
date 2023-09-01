import grin
from grin.execution import Execution
from grin.types import GrinVar, grin_object_from_value, GrinString


# The statements module contains classes for each possible grin statement, such as
# a let statement, an add statement, a goto statement, etc. All methods have slightly
# different implementations but share an interface that contains an execute() method,
# such that each statement can be executed. The underlying execute() method takes in
# an execution object, allowing variables, labels, and the current line to be changed
# accordingly.



class GrinTypeError(Exception):
    """The GrinTypeError is an exception raised when there is an invalid operation performed between
    two different grin types."""
    def __init__(self, error = None, *, message = None):
        self._error = error
        if not message:
            self._message = self._create_message()
        else: self._message = message

    def __str__(self):
        return f'GrinTypeError: {self._message}'

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




class GrinValueError(ValueError):
    """The GrinValueError is an exception that is raised when strings are placed into int() or
    float() functions."""
    def __init__(self, error = None, *, message = None):
        self._error = error
        if message:
            self._message = message
        else:
            self._message = self._create_message()

    def __str__(self):
        return f'GrinValueError: {self._message}'

    def _create_message(self) -> None:
        """Replaces python terms for grin terms in the error message"""
        message = str(self._error)
        while 'int' in message:
            return message[:message.index('int')] + 'GrinInt' + message[
                                                                      message.index('int') + 3:]
        while 'float' in message:
            return message[:message.index('float')] + 'GrinFloat' + message[
                                                                       message.index('float') + 5:]


class GrinGoError(Exception):
    """The GrinGoError encompasses all exceptions that are raised during execution or creation
    of a Go (GoTo, GoSub) statement."""
    def __init__(self, error: Exception):
        self._error = error

    def __str__(self):
        return f'GrinGoError: {self._error}'




class Let:
    """The Let statement is one in which two values are stored, and when the execution method is
    called, the Let statement creates a variable with the name of the first value and gives it
    the value of the second value"""
    def __init__(self, variable: str, value: "GrinType"):
        self._var = None
        self._variable = variable
        self._value = value

    def var(self) -> GrinVar:
        return self._var

    def test(self) -> GrinVar:
        self._var = GrinVar(self._variable, self._value)
        return self.var()

    def execute(self, execution: Execution):
        if self._value in execution.vars().keys():
            self._value = execution.vars()[self._value].name()

        self._var = GrinVar(self._variable, self._value)
        execution._conversion_obj._vars[self._variable] = self._var
        execution._vars[self._variable] = self._var
        return 1

class Print:
    """The Print statement is one in which a value (GrinVar, GrinInt, GrinFloat) is stored,
    and the execute method prints the value to the console, making sure to adjust GrinVars to
    their values rather than their names"""
    def __init__(self, value: "GrinVal"):
        self._value = value
        self._tv = None

    def event(self) -> "GrinVal":
        return self._event

    def test(self):
        self._tv = self._value
        self._create_statement()
        return self._value.value()


    def execute(self, execution: Execution):
        if self._value in execution.vars().keys():
            if execution.vars()[self._value].value() in execution.vars().keys():
                self._tv = execution.vars()[execution.vars()[self._value].value()]
                while execution.vars()[self._tv.name()].value() in execution.vars().keys():
                    self._tv = execution.vars()[execution.vars()[self._tv.name()].value()]
            else:
                self._tv = execution.vars()[self._value].value()
        else:
            self._tv = self._value
        self._create_statement()
        print(self._event)
        return 1

    def _create_statement(self):
        if isinstance(self._tv, GrinVar):
            self._event = f'{self._tv.value()}'
        else:
            self._event = f'{self._tv}'



class Instr:
    """An Instr statement is one that contains a name for a variable and, once executed,
    allows the user to type a string value and insert a value into that same variable"""
    def __init__(self, name: str):
        self._name = name

    def var(self):
        return GrinVar(self._name, self._value)

    def test(self, input: str):
        self._value = input
        return self.var()

    def execute(self, execution: Execution):
        _value = str(input().strip())
        execution._vars[self._name] = GrinVar(self._name, _value)
        return 1

class Innum:
    """An Innum statement is one that contains a name for a variable and, once executed,
    allows the user to type an int or float value and insert a value into that same variable"""
    def __init__(self, name: str):
        self._name = name

    def item(self) -> GrinVar:
        return GrinVar(self._name, self._value)

    def test(self, input: str) -> GrinVar:
        self._value = self._float_or_int(input)
        return self.item()
    def execute(self, execution: Execution) -> None:
        _value = input().strip()
        self._value = self._float_or_int(_value)
        execution._vars[self._name] = GrinVar(self._name, self._value)
        return 1

    def _float_or_int(self, value: str) -> None | GrinValueError:
        if '_' in value:
            raise GrinValueError(message = "'_' is an invalid character")
        if ',' in value:
            raise GrinValueError(message = "',' is an invalid character")

        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError as error:
            raise GrinValueError(error)



class Add:
    """The Add statement contains two values, and once executed, augments the first value with the
    addition of the second. The Add statement (and likewise arithmetic operations), must first
    adjust GrinVars for their values"""

    def __init__(self, var: str, value: "GrinVal"):
        self._var = var
        self._value = value

    def var(self) -> GrinVar:
        return self._var

    def test(self) -> GrinVar:
        self._add_to_var()
        return self.var()

    def execute(self, execution: Execution) -> int:
        self._var = execution.vars()[self._var]

        if isinstance(self._value, GrinString):
            if self._value.value() in execution._vars.keys():
                self._value = execution._vars[self._value.value()]

        while isinstance(self._value, GrinVar):
            if self._value.name() in execution._vars.keys():
                self._value = grin_object_from_value(execution._vars[self._value.name()].value())


        self._add_to_var()
        return 1

    def _add_to_var(self) -> None:
        try:
            self._var.add(self._value)
        except TypeError as error:
            raise GrinTypeError(error)



class Sub:
    """The Sub statement contains two values, and once executed, subtracts the second value from the
    first value, updating the first value in the execution instance"""
    def __init__(self, var: str, value: "GrinVal"):
        self._var = var
        self._value = value

    def var(self) -> GrinVar:
        return self._var

    def test(self) -> GrinVar:
        self._subtract_from_var()
        return self.var()

    def execute(self, execution: Execution) -> int:
        self._var = execution.vars()[self._var]
        if isinstance(self._value, GrinVar):
            if self._value.name() in execution._vars.keys():
                self._value = grin_object_from_value(execution._vars[self._value.name()].value())
        self._subtract_from_var()
        return 1

    def _subtract_from_var(self):
        try:
            self._var.subtract(self._value)
        except TypeError as error:
            raise GrinTypeError(error)



class Mult:
    """The Mult statement contains two values, and multiplies the first value by the second value
    when executed"""
    def __init__(self, var: str, value: "GrinVal"):
        self._var = var
        self._value = value

    def var(self) -> GrinVar:
        return self._var

    def test(self) -> GrinVar:
        self._multiply_var()
        return self.var()
    def _multiply_var(self) -> None:
        self._var.multiply(self._value)

    def execute(self, execution: Execution) -> int:
        self._var = execution.vars()[self._var]

        if isinstance(self._value, GrinString):
            if self._value.value() in execution._vars.keys():
                self._value = execution._vars[self._value.value()]

        while isinstance(self._value, GrinVar):
            if self._value.name() in execution._vars.keys():
                self._value = grin_object_from_value(execution._vars[self._value.name()].value())



        self._multiply_var()
        return 1


class Execution:
    pass


class Div:
    """The Div statement contains two values, and divides the second value by the first value
    when executed."""
    def __init__(self, var: str, value: "GrinVal"):
        self._var = var
        self._value = value

    def var(self) -> GrinVar:
        return self._var

    def test(self) -> GrinVar:
        self._divide_var()
        return self.var()

    def execute(self, execution: Execution) -> int:
        self._var = execution.vars()[self._var]
        if isinstance(self._value, GrinVar):
            if self._value.name() in execution._vars.keys():
                self._value = grin_object_from_value(execution._vars[self._value.name()].value())
        self._divide_var()
        return 1

    def _divide_var(self) -> None:
        self._var.divide(self._value)




class Go:
    """The Go class is a superclass in which two derived classes, the GoTo and GoSub classes, inherit
    their underlying meaning from. Objects of a Go class contain a conversion_objects (an instance
    of grin code and all of its details), a target, and a conditional statement which is by default
    None."""
    def __init__(self, conversion_obj: "Conversion", target: int | str, *, conditional_statement = None):
        self._conversion_obj = conversion_obj
        self._target = target
        self._conditional_statement = conditional_statement
    def _check_if_true(self, execution: Execution) -> bool:
        return self._conditional_statement.is_true(execution)

    def _adjust_for_vars(self, execution: Execution) -> None:
        _pvar = self._conditional_statement.first_value().value()
        if _pvar in execution.vars().keys():
            self._conditional_statement.change_first_value(execution.vars()[_pvar])

    def _adjust_for_execution(self, execution: Execution) -> None:
        self._conversion_obj = execution._conversion_obj


    def _check_if_zero(self, value: int | float) -> bool | GrinGoError:
        if value != 0:
            return True
        else:
            raise GrinGoError('GOTO statement cannot be zero')

    def _check_goto_out_of_bounds(self, execution: Execution, value: "GrinVal") -> None | Exception:
        if type(value) == str:
            raise GrinGoError('GOTO specified label that did not exist')
        else:
            _index = value + execution.index() - 1
            if _index < 0 or _index >= len(execution.grin_code()):
                raise GrinGoError('GOTO statement leads to a line not within the bounds of the program')

    def _check_gosub_out_of_bounds(self, execution: Execution, value: "GrinVal") -> None | Exception:
        if type(value) == str:
            raise GrinGoError('GOTO specified label that did not exist')
        else:
            if value < 0 or value >= len(execution.grin_code()):
                raise GrinGoError('GOTO statement leads to a line not within the bounds of the program')

    def _check_float_error(self, value: "GrinVal") -> None | Exception:
        if isinstance(value, float):
            raise GrinTypeError("list indices must be GrinInt, not GrinFloat")

    def _return_line_if_conditional_statement_exists(self, execution: Execution) -> int:
        self._adjust_for_vars(execution)
        if self._check_if_true(execution):
            if self._target in execution._labels.keys():
                _line = execution._labels[self._target].line() - execution._index + 1
            elif self._target in execution._vars.keys():
                _line = execution.vars()[self._target].value()
            else:
                _line = self._target
            self._check_if_zero(_line)
            self._check_goto_out_of_bounds(execution, _line)
        else:
            _line = 1

        self._check_float_error(_line)
        return _line

    def _return_line_if_conditional_statement_does_not_exist(self, execution: Execution) -> int:
        self._adjust_for_execution(execution)
        if self._target in execution._labels.keys():
            _line = execution._labels[self._target].line() - execution._index + 1
        elif self._target in execution._vars.keys():
            if execution.vars()[self._target].value() in execution._labels.keys():
                _line = execution._labels[execution.vars()[self._target].value()].line() - execution._index + 1
            else:
                _line = execution.vars()[self._target].value()
        else:
            _line = self._target

        self._check_float_error(_line)
        self._check_if_zero(_line)
        self._check_goto_out_of_bounds(execution, _line)
        return _line


class GoTo(Go):
    """The GoTo statement adjusts the current line of an execution, making sure that both
    the conditional (if exists) is true, and that there are no errors such as a target equal to 0"""
    def execute(self, execution = None) -> int:
        if self._conditional_statement:
            return self._return_line_if_conditional_statement_exists(execution)
        else:
            return self._return_line_if_conditional_statement_does_not_exist(execution)


class GoSub(Go):
    """The GoSub statement recursively creates and executes new execution objects with the line
    adjusted as a method of jumping (ahead or behind) the current line, and returning back to the
    current line once a Return has been reached."""

    def execute(self, execution = None) -> int:
        _index = 0
        if self._conditional_statement:
            self._adjust_for_vars(execution)
            self._adjust_for_execution(execution)
            if self._check_if_true(execution):
                if self._target in execution._labels.keys():
                    return self._perform_recursive_execution(execution, execution._labels[self._target].line() + 1)

                else:
                    return self._perform_recursive_execution(execution, execution._index + self._target)
            else:
                return 1
        else:
            self._adjust_for_execution(execution)
            if self._target in execution._labels.keys():
                return self._perform_recursive_execution(execution, execution._labels[self._target].line() + 1)
            else:
                return self._perform_recursive_execution(execution, execution._index + self._target)



    def _perform_recursive_execution(self, execution, _index: int) -> int:
        self._check_gosub_out_of_bounds(execution, _index)
        grin.Execution(self._conversion_obj, index = _index).execute()
        return 1

class Return:
    """A Return object is one that specifies a Return token"""
    pass

class End:
    """An End object is one that specifies a Dot (.) Token, which signifies the end of a program
    running"""
    pass


__all__ = [
    GrinTypeError.__name__,
    GrinValueError.__name__,
    GrinGoError.__name__,
    Let.__name__,
    Print.__name__,
    Instr.__name__,
    Innum.__name__,
    Add.__name__,
    Sub.__name__,
    Mult.__name__,
    Div.__name__,
    Go.__name__,
    GoTo.__name__,
    GoSub.__name__,
    Return.__name__,
    End.__name__
]


