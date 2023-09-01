from event_list import EventList

# A device is an object that contains a propagate-list, an id, and
# a dictionary of cancels. The propagate-list will be a list of tuples
# containing the device to which it sends events to, and the delay before
# that sent event is received. The device id is unique to every device, and
# cancels dictionary is one that contains cancels (message, time), such that
# other modules can utilize this to stop any events from being sent from this
# device if it already knows about a cancel.


class Device:
    def __init__(self, device_id):
        self._device_id = device_id
        self._propagate_list = []
        self._cancels = dict()


    def device_id(self) -> int:
        """Returns the device's id"""
        return self._device_id

    def add_cancel(self, message: str, time: int) -> None:
        """Adds a cancel to the device's cancel list. The
           structure of a cancel is (message, time)"""
        self._cancels[message] = time

    def cancels(self) -> None:
        """Returns the cancels of a device if it contains one. A device
           either has a cancel from the initial cancel or receives it
           from another device through the simulation"""
        return self._cancels
    def propagate_list(self) -> list:
        """Returns the propagate list of a device"""
        return self._propagate_list[:]

    def add_propagate(self, device: "device") -> None:
        """Adds a device to the devices propagate list"""
        self._propagate_list.append(device)
        self._sort_propagate_list()

    def send_alert(self, event_list: EventList, device: int, message: str, time: int, delay: int) -> list:
        """Adds two events: one for sending the act of device 1 sending
           an alert to device 2, and the other for device 2 receiving that
           alert from device 1"""
        event_list.add_event(time - delay, self.device_id(), device, message, alert = True, sender = True)
        event_list.add_event(time, device, self.device_id(), message, alert = True)

    def send_cancel(self, event_list: EventList, device: int, message: str, time: int, delay: int) -> list:
        """Adds two events: one for sending the act of device 1 sending
           a cancel to device 2, and the other for device 2 receiving that
           cancel from device 1"""
        event_list.add_event(time - delay, self.device_id(), device, message, cancel = True, sender = True)
        event_list.add_event(time, device, self.device_id(), message, alert = False, cancel = True)

    def _sort_propagate_list(self) -> None:
        """This method will sort a propagate list in order
           of smallest delay to the largest delay"""
        times = []
        for device, delay in self._propagate_list:
            times.append(delay)

        times.sort()
        temp = []

        for time in times:
            for device, delay in self._propagate_list:
                if delay == time:
                    temp.append((device, delay))

        self._propagate_list = temp



