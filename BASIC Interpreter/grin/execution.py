import grin

# The execution module contains a class, called Execution, that handles the
# execution of a sequence of grin code after it has been converted into
# executable statements. An execution object will contain information that
# is necessary for the running of the script, including the current line
# number, the status of whether the program is currently inside a
# GoSub statement, as well as all the labels and the variables.


class Execution:
    def __init__(self, conversion_obj: "Conversion", *, index = 1, gosub = True):
        self._gosub = gosub
        self._conversion_obj = conversion_obj
        self._index = index
        self._grin_code = conversion_obj.grin_code()
        self._vars = conversion_obj._vars
        self._labels = conversion_obj._labels

    def index(self) -> None:
        """Returns the current index (line number) of an execution object"""
        return self._index

    def grin_code(self) -> None:
        """Returns the grincode of an execution object"""
        return self._grin_code[:]

    def gosub_status(self) -> None:
        """Returns true when inside a GoSub statement; false otherwise"""
        return self._gosub

    def turn_off_gosub(self) -> None:
        """Makes the gosub attribute falsy"""
        self._gosub = False

    def turn_on_gosub(self) -> None:
        """Makes the gosub attribute truthy"""
        self._gosub = True

    def vars(self) -> dict:
        """Returns a dictionary containing of variables of an execution object"""
        return self._vars

    def labels(self) -> dict:
        """Returns a dictionary containing the labels of an execution objects"""
        return self._labels
    def execute(self) -> None:
        """Main method that executes a sequence of grincode"""
        while self._index <= len(self._grin_code):
            if type(self._grin_code[self._index - 1]) == grin.GrinReturn:
                if self.gosub_status():
                    self.turn_off_gosub()
                    return
                else:
                    raise grin.GrinGoError("Return statement reached without the presence of GoSub")
                    quit()
            elif type(self._grin_code[self._index - 1]) == grin.GrinEnd:
                quit()
            else:
                self._index += self._grin_code[self._index - 1].execute(self)



__all__ = [
    Execution.__name__
]



