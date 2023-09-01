
# The console module contains all classes responsible for reading and converting
# grin code into executable grin statements. There are two main class: the Interface, and the
# Conversion.


from grin import lexing, parsing, comparisons, GrinToken
from grin.statements import *
from grin.types import grin_object_from_value, GrinReturn, GrinEnd, GrinLabel, GrinVar


class GrinTypeError(Exception):
    """A GrinTypeError is a special exception raised for a specific instance in which an grin
    syntax error is not caught prior to execution"""
    def __init__(self, mistake: str):
        self._mistake = mistake

    def __str__(self):
        return f'{self._mistake} is not contained by double parenthesis'




class Interface:
    """The interface object reads input from the user and has method that can either parse
    or lex the input. For our purposes, parsing will be used more often than not."""

    def __init__(self):
        self._code = None
    def read_input(self) -> None:
        """Returns a list of all user inputted statements"""
        self._code = self._read_all_input()

    def parse_input(self) -> None:
        """Parses the code stored in the object"""
        return self._parse_input(self._code)

    def lex_input(self) -> None:
        """Lexes the code stored in the object"""
        return self._lex_input(self._code)

    def _read_all_input(self) -> list[str]:
        """Reads input from the user until a DOT is entered, returning a list
        containing all lines."""
        temp = []
        while True:
            line = self._get_text()
            if line != '.':
                temp.append(line)
            else:
                temp.append(line)
                break
        return temp

    def _parse_input(self, lines_of_code: str) -> "Parsed code":
        return parsing.parse(lines_of_code)


    def _lex_input(self, lines_of_code) -> "Lexed code":
        index = 1
        for line in lines_of_code:
                yield lexing.to_tokens(line, index)
                index += 1

    def _get_text(self) -> str:
        return str(input().strip())



class Conversion:
    """The Conversion class handles all conversions between inputted grin code and executable
    grin statements. By iteration line by line, the Conversion object stores necessary information
    such as the grin code (organized by list), the variables and the labels of a grin program."""
    def __init__(self, parsed_code: "iterable[GrinToken]"):
        self._grin_code = []
        self._parsed_code = parsed_code
        self._vars = dict()
        self._labels = dict()
        self._current = 1

    def grin_code(self) -> "GrinCode":
        return self._grin_code[:]

    def vars(self) -> dict:
        return self._vars

    def labels(self) -> dict:
        return self._labels

    def convert(self) -> None:
        """Converts parsed code to a sequence of executable statements."""
        for line in self._parsed_code:
            token = line[0]
            self._convert_line(token, line)

    def _convert_line(self, token, line) -> None:
        token_id = token.kind().index()
        if token_id == 1:
            self._handle_add_statement(line)
        elif token_id == 3:
            self._handle_div_statement(line)
        elif token_id == 5:
            self._handle_end_statement(line)
        elif token_id == 7:
            self._handle_gosub_statement(line)
        elif token_id == 8:
            self._handle_goto_statement(line)
        elif token_id == 11 and line[1].kind().index() == 2:
            self._handle_label_statement(line)
        elif token_id == 13:
            self._handle_innum_statement(line)
        elif token_id == 14:
            self._handle_instr_statement(line)
        elif token_id == 17:
            self._handle_let_statement(line)
        elif token_id == 21:
            self._handle_mult_statement(line)
        elif token_id == 23:
            self._handle_print_statement(line)
        elif token_id == 24:
            self._handle_return_statement(line)
        elif token_id == 25:
            self._handle_sub_statement(line)

    def _var_from_name(self, name)-> GrinVar:
        return self._vars[name]

    def _handle_add_statement(self, line: "iterable(GrinToken)") -> None:
        self._grin_code.append(Add(line[1].text(), self._return_grin_obj(line[2].value())))
        self._vars[line[1].text()] = GrinVar(line[1].text(), 0)

    def _handle_gosub_statement(self, line: "iterable(GrinToken)") -> None:
        if len(line) > 2:
            self._grin_code.append(GoSub(self, line[1].value(), conditional_statement = comparisons.create_comparison([line[2:]])))
        else:
            self._grin_code.append(GoSub(self, line[1].value()))

    def _handle_goto_statement(self, line: "iterable(GrinToken)") -> None:
        if len(line) > 2:
            self._grin_code.append(GoTo(self, line[1].value(), conditional_statement = comparisons.create_comparison(line[2:])))
        else:
            self._grin_code.append(GoTo(self, line[1].value()))
    def _handle_label_statement(self, line: "iterable(GrinToken)") -> None:
        self._convert_line(line[2], line[2:])
        self._labels[line[0].value()] = GrinLabel(line[0].text(), len(self._grin_code))
    def _handle_innum_statement(self, line: "iterable(GrinToken)") -> None:
        self._grin_code.append(Innum(line[1].text()))

    def _handle_return_statement(self, line: "iterable(GrinToken)") -> None:
        self._grin_code.append(GrinReturn())
    def _handle_instr_statement(self, line: "iterable(GrinToken)") -> None:
        self._grin_code.append(Instr(line[1].text()))
    def _handle_div_statement(self, line: "iterable(GrinToken)") -> None:

        self._grin_code.append(Div(line[1].text(), self._return_grin_obj(line[2].value())))
        self._vars[line[1].text()] = GrinVar(line[1].text(), 0)
    def _handle_mult_statement(self, line: "iterable(GrinToken)") -> None:
        self._grin_code.append(Mult(line[1].text(), self._return_grin_obj(line[2].value())))
        self._vars[line[1].text()] = GrinVar(line[1].text(), 0)
    def _handle_sub_statement(self, line: "iterable(GrinToken)") -> None:
        self._grin_code.append(Sub(line[1].text(), self._return_grin_obj(line[2].value())))
        self._vars[line[1].text()] = GrinVar(line[1].text(), 0)
    def _handle_print_statement(self, line: "iterable(GrinToken)") -> None:
        val = line[1].value()
        self._vars[line[1].text()] = GrinVar(line[1].text(), 0)
        self._grin_code.append(Print(val))
    def _handle_let_statement(self, line: "iterable(GrinToken)") -> None:
        self._check_for_let_errors(line[2])
        let_statement = Let(line[1].text(), line[2].value())
        self._grin_code.append(let_statement)
        self._vars[line[1].text()] = GrinVar(line[1].text(), 0)

    def _handle_end_statement(self, line: "iterable(GrinToken)") -> None:
        self._grin_code.append(GrinEnd())

    def _return_grin_obj(self, val: str) -> "GrinVal":
        if val in self._vars.keys():
            return self._vars[val]
        else:
            return grin_object_from_value(val)

    def _check_for_let_errors(self, value: GrinToken) -> None | Exception:
        if value.kind().index() == 11:
            self._vars[value.value()] = GrinVar(value.value(), 0)



__all__ = [
    GrinTypeError.__name__,
    Interface.__name__,
    Conversion.__name__
]



