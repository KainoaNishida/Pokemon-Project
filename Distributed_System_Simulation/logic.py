# This module handles the progression of a simulation,
# including getting all events starting with an initial one,
# and printing output. Recursion is used extensively in this
# module.

from device import Device
from event_list import EventList
from file_handling import FileHandler, alert, cancel
from collections import namedtuple # this might be sus but imma leave it here

class Run():
    def __init__(self, file_handler: FileHandler):
        self._events = [] # this will be a list of event_lists
        self._file_handler = file_handler

    def events(self):
        """returns the list of event, each element being an EventList object"""
        return self._events[:]

    def all_event_messages(self):
        """returns a list containing all alert/cancel messages, since
           a simulation can have more than one event occuring at the same
           time"""
        temp = []
        for event in self._events:
            temp.append(event.name())
        return temp

    def event_with_message(self, message):
        """returns the EventList of a specific message"""
        for event in self._events:
            if event.name() == message:
                return event


    def get_all_events(self) -> None:
        """A method that recursively handles the simulation by
           starting with a cancel or alert, sending that event to
           each device in the starting device's propagation list,
           and doing so until a cancel has been received. Does this
           for every alert/cancel event."""

        for cancel in self._file_handler.cancels():
            el = EventList(cancel.message)
            self.recursive_cancel_events(el, cancel)

        for alert in self._file_handler.alerts():
            if alert.message in self.all_event_messages():
                el = self.event_with_message(alert.message)
            else:
                el = EventList(alert.message)
            self.recursive_alert_events(el, alert)


        el.delete_events_post_simulation(self._file_handler.length())
        el.add_event(self._file_handler.length(), 1, 2, None, alert = False, cancel = False)

        el.sort(self._file_handler.length())



    def recursive_alert_events(self, event_list, initial_alert) -> None:
        """Recursively adds all alert events by sending the initial
           alert from the starting device to every device in its
           propagation list, and doing so until a cancel has been received"""
        id, message, time = initial_alert

        if time < self._file_handler.length():
            if not message in self._file_handler.device(id).cancels().keys():
                self._file_handler.device(id).add_cancel(message, self._file_handler.length())

            for device, delay in self._file_handler.device(id).propagate_list():
                if time < self._file_handler.device(id).cancels()[message]:
                    self._file_handler.device(id).send_alert(event_list, device, message, time + delay, delay)
                    self.recursive_alert_events(event_list, alert(self._file_handler.device(device).device_id(), message, time + delay))

        if not (message in self.all_event_messages()):
            self._events.append(event_list)


    def recursive_cancel_events(self, event_list, initial_cancel) -> None:
        """Recursively adds all cancel events by sending the initial
           cancel from the starting device to every device in its
           propagation list, and doing so until a cancel has been received
           by every device"""

        id, message, time = initial_cancel

        if not (message in self._file_handler.device(id).cancels().keys()):
            self._file_handler.device(id).add_cancel(message, time)

            for device, delay in self._file_handler.device(id).propagate_list():
                if not (message in self._file_handler.device(device).cancels().keys()):
                    self._file_handler.device(id).send_cancel(event_list, device, message, time + delay, delay)
                    self.recursive_cancel_events(event_list, cancel(self._file_handler.device(device).device_id(), message, time + delay))
                else:
                    self._file_handler.device(id).send_cancel(event_list, device, message, time + delay, delay)

        if not (message in self.all_event_messages()):
            self._events.append(event_list)

def print_output(time: int, device1_id: int, device2_id: int, message: str, alert = False, cancel = False, sender = False) -> None:
    """Takes in a tuple containing the information about an event and prints
       it out according to a specific format. The input tuples should be as follows:
       (time, id1, id2, message, alert, cancel, sender)"""

    if (alert == False) and (cancel == False):
        print(f'@{time}: END')

    else:
        if alert:
            if sender:
                print(f'@{time}: #{device1_id} SENT ALERT TO #{device2_id}: {message}')
            else:
                print(f'@{time}: #{device1_id} RECEIVED ALERT FROM #{device2_id}: {message}')
        else:
            if sender:
                print(f'@{time}: #{device1_id} SENT CANCELLATION TO #{device2_id}: {message}')
            else:
                print(f'@{time}: #{device1_id} RECEIVED CANCELLATION FROM #{device2_id}: {message}')

