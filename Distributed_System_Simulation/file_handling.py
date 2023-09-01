from pathlib import Path
from device import *
from collections import namedtuple

# This module will handle opening and reading the
# information from a file, which includes going
# through line by line and storing the data.

propagate = namedtuple('propagate', ['id', 'delay'])
alert = namedtuple('alert', ['id1', 'message', 'delay'])
cancel = namedtuple('cancel', ['id1', 'message', 'delay'])
class FileHandler:

    def __init__(self):
        self._length = 0
        self._devices = set()
        self._alerts = set()
        self._cancels = set()

    def length(self) -> int:
        """Returns the length of a simulation"""
        return self._length

    def devices(self) -> set:
        """Returns a set containing devices"""
        return self._devices

    def cancels(self) -> set:
        """Returns a set containing initial cancel events"""
        return self._cancels

    def alerts(self) -> set:
        """Returns a set containing initial alert events"""
        return self._alerts

    def device(self, device_id) -> Device:
        """Returns a device from a specified id"""
        for device in self._devices:
            if device.device_id() == device_id:
                return device

    def open_file(self, path: Path) -> None:
        """Opens a file and handles each
           line of the file, storing that line
           as information or discarding it if it is
           a comment of empty space"""
        with open(path, mode = 'r') as file:
            for line in file:
                self._handle_line(line)


    def _handle_line(self, text: str) -> None:
        """Handles each line of text in a file, either
           storing the information or ignoring it"""
        _text = text.strip()
        if _text:
            if _text.startswith('LENGTH'):
                self._length = _return_length(_text)
            elif _text.startswith('DEVICE'):
                self._devices.add(_return_device(_text))
            elif _text.startswith('PROPAGATE'):
                self._handle_propagate(_text)
            elif text.startswith('ALERT'):
                self._add_alert(_text)
            elif text.startswith('CANCEL'):
                self._add_cancel(_text)
            else:
                pass
        else:
            pass

    def _handle_propagate(self, text: str) -> None:
        """Adds to the propagate attribute of a device, unique by its id"""
        _first_id, _second_id, _delay = [int(i) for i in text.split()[1:]]
        for device in self._devices:
            if device.device_id() == _first_id:
                device.add_propagate(propagate(_second_id, _delay))

    def _add_alert(self, text: str) -> None:
        """Adds a tuple with the first element containing the device id, the second
        containing message, and the third containing the time to the alert list"""
        device_id, message, time = text.split()[1:]
        self._alerts.add(alert(int(device_id), message, int(time)))

    def _add_cancel(self, text: str) -> None:
        """Adds a tuple with the first element containing the device id, the second
        containing message, and the third containing the time to the cancel list"""
        device_id, message, time = text.split()[1:]
        self._cancels.add(cancel(int(device_id), message, int(time)))

def _return_length(text: str) -> int:
    """Returns the non-negative integer following the word LENGTH in a file"""
    return int(text.split()[1]) * 60000

def _return_device(text: str) -> Device:
    """returns a device with all of its attributes"""
    _device_id = int(text.split()[1])
    return Device(_device_id)






