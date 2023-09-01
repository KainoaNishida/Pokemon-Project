
# This module will contain the EventList calls, in which objects of this class
# will have a few methods, namely sorting. Objects of the EventList class will be
# unique by their message, meaning all events are process according to their message.
# This will then be used by other modules to combine all EventLists and process them
# together to model the simulation.




class EventList:
    def __init__(self, message):
        self._name = message
        self._event_list = []
    def name(self) -> str:
        """Returns name"""
        return self._name

    def event_list(self) -> list:
        """Returns EventList"""
        return self._event_list[:]

    def sort(self, endtime) -> None:
        """Sorts the EventList"""
        self._sort_times(endtime)
        self._sort_details()

    def _sort_details(self) -> None:
        """Since the project contains very specific details
           regarding the order in which events are send and received,
           this method sorts the EventList according
           to the rules one by one"""
        self._sort_receives_before_sends()
        self._sort_devices_recieve_message_at_same_time()
        self._sort_receive_cancels_before_alerts()
        self._sort_lexicographically()
        self._sort_sending_from_same_device()
        self._sort_sending_from_different_devices()
        self._sort_send_cancels_before_alerts()

    def _sort_sending_from_different_devices(self) -> None:
        """Ensures that device with lower id sends alert/cancel first"""
        for i in range(len(self._event_list)):
            for j in range(i + 1, len(self._event_list)):
                if both_have_same_time(self._event_list[i], self._event_list[j]):
                    if both_sending(self._event_list[i], self._event_list[j]):
                        if both_different_devices(self._event_list[i], self._event_list[j]):
                            if both_alert(self._event_list[i], self._event_list[j]) or both_cancel(self._event_list[i], self._event_list[j]):
                                if is_first_id_greater(self._event_list[i], self._event_list[j]):
                                    self._event_list[i], self._event_list[j] = self._event_list[j], \
                                        self._event_list[i]
    def _sort_receive_cancels_before_alerts(self) -> None:
        """Ensures that cancels are received by a device before alerts
           if they are scheduled to occur at the same time"""
        for i in range(len(self._event_list)):
            for j in range(i + 1, len(self._event_list)):
                if both_have_same_time(self._event_list[i], self._event_list[j]):
                    if both_receiving(self._event_list[i], self._event_list[j]):
                        if both_same_device(self._event_list[i], self._event_list[j]):
                            if first_is_alert_and_second_is_cancel(self._event_list[i], self._event_list[j]):
                                self._event_list[i], self._event_list[j] = self._event_list[j], self._event_list[i]

    def _sort_send_cancels_before_alerts(self) -> None:
        """Ensures that cancels are sent by a device before alerts
        if they are scheduled to occur at the same time"""
        for i in range(len(self._event_list)):
            for j in range(i + 1, len(self._event_list)):
                if both_have_same_time(self._event_list[i], self._event_list[j]):
                    if both_sending(self._event_list[i], self._event_list[j]):
                        if first_is_alert_and_second_is_cancel(self._event_list[i], self._event_list[j]):
                            self._event_list[i], self._event_list[j] = self._event_list[j], self._event_list[i]


    def _sort_lexicographically(self) -> None:
        """Ensures that messages are sorted lexicographically if alerts/cancels
           with different messages are sent/received at same time"""
        for i in range(len(self._event_list)):
            for j in range(i + 1, len(self._event_list)):
                if both_have_same_time(self._event_list[i], self._event_list[j]):
                    if both_receiving(self._event_list[i], self._event_list[j]):
                        if both_same_device(self._event_list[i], self._event_list[j]):
                            if both_alert(self._event_list[i], self._event_list[j]) or both_cancel(self._event_list[i], self._event_list[j]):
                                if is_second_message_greater_than_first(self._event_list[i], self._event_list[j]):
                                    self._event_list[i], self._event_list[j] = self._event_list[j], \
                                    self._event_list[i]
    def _sort_sending_from_same_device(self) -> None:
        """Ensures that device sends cancel/alert to device with lower id"""
        for i in range(len(self._event_list)):
            for j in range(i + 1, len(self._event_list)):
                if both_have_same_time(self._event_list[i], self._event_list[j]):
                    if both_sending(self._event_list[i], self._event_list[j]):
                        if both_same_device(self._event_list[i], self._event_list[j]):
                            if both_alert(self._event_list[i], self._event_list[j]) or both_cancel(self._event_list[i], self._event_list[j]):
                                if is_second_id_greater(self._event_list[i], self._event_list[j]):
                                    self._event_list[i], self._event_list[j] = self._event_list[j], \
                                    self._event_list[i]
    def _sort_devices_recieve_message_at_same_time(self) -> None:
        """Ensures that device with lower id receives cancel/alert first"""
        for i in range(len(self._event_list)):
            for j in range(i + 1, len(self._event_list)):
                if both_have_same_time(self._event_list[i], self._event_list[j]):
                    if both_receiving(self._event_list[i], self._event_list[j]):
                        if is_first_id_greater(self._event_list[i], self._event_list[j]):
                            self._event_list[i], self._event_list[j] = self._event_list[j], self._event_list[i]


    def _sort_receives_before_sends(self) -> None:
        """Ensures that all events are received before sent"""
        for i in range(len(self._event_list)):
            for j in range(i + 1, len(self._event_list)):
                if both_have_same_time(self._event_list[i], self._event_list[j]):
                    if is_sender(self._event_list[i]):
                        if not is_sender(self._event_list[j]):
                            el = self._event_list[j]
                            self._event_list.pop(j)
                            self._event_list.insert(i, el)

    # The base case of this function involves time > endtime, which was a possibility
    # when I first began this project. However, since I used recursion instead and stopped
    # sending alerts/cancels immediately when a cancel is known by a device, this case
    # should theoretically never happen.
    def _sort_times(self, endtime: int) -> None:
        """This method sorts the events in the EventList
           according to their time, without regards to any of the
           rules"""
        times = set()
        _new_event_list = []

        for event in self._event_list:
            times.add(int(event[0]))  # This is time

        times = list(times)
        times.sort()

        for time in times:
            if time > endtime:
                pass
            else:
                for event in self._event_list:
                    if event[0] == time:
                        _new_event_list.append(event)

        self._event_list.clear()
        self._event_list = _new_event_list


    def delete_events_post_simulation(self, end_time: int) -> None:
        """This method deletes all events that have a time that is
           larger than the end time. However, since this was written
           prior to pursuing a recursive algorithm, this method is not
           implemented anywhere yet"""

        temp = self._event_list[:]
        for event in self._event_list:
            if int(event[0]) >= end_time:
                temp.remove(event)

        self._event_list = temp

    def add_event(self, time: int, id1: int, id2: int, message: str, *, alert = False, cancel = False, sender = False) -> None:
        """Adds an event to the EventList"""
        self._event_list.append((time, id1, id2, message, alert, cancel, sender))



# Below are multiple functions that returns boolean
# values depending on a very specific scenario. These either
# take in two events as input and compare a value in both of them,
# or take in a single event and returns a specific value in it, such as
# whether or not it is an alert.

def both_receiving(first_event: "event", second_event: "event") -> bool:
    return not (first_event[6]) and not (second_event[6])
def first_is_alert_and_second_is_cancel(first_event: "event", second_event: "event") -> bool:
    return first_event[4] and second_event[5]
def both_sending(first_event: "event", second_event: "event") -> bool:
    return (first_event[6]) and (second_event[6])
def both_have_same_time(first_event: "event", second_event: "event") -> bool:
    return first_event[0] == second_event[0]
def both_same_device(first_event: "event", second_event: "event") -> bool:
    return first_event[1] == second_event[1]
def both_different_devices(first_event: "event", second_event: "event") -> bool:
    return first_event[1] != second_event[1]
def both_cancel(first_event: "event", second_event: "event") -> bool:
    return first_event[5] and second_event[5]
def both_alert(first_event: "event", second_event: "event") -> bool:
    return first_event[4] and second_event[4]
def is_alert(event: "event") -> bool:
    return event[4]
def is_second_id_greater(first_event: "event", second_event: "event") -> bool:
    return first_event[2] > second_event[2]
def is_first_id_greater(first_event: "event", second_event: "event") -> bool:
    return first_event[1] > second_event[1]
def is_second_message_greater_than_first(first_event: "event", second_event: "event") -> bool:
    return first_event[3] > second_event[3]
def is_cancel(event: "event") -> bool:
    return event[5]
def is_sender(event: "event") -> bool:
    return event[6]
