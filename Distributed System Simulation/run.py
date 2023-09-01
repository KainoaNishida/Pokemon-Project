from pathlib import Path

import logic
from event_list import EventList
from file_handling import FileHandler
from logic import Run


def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input())

def combine_all_events_into_single_event_list(file_handler: FileHandler) -> EventList:
    runner = EventList('run')
    run = Run(file_handler)
    run.get_all_events()

    for event_list in run.events():
        for event in event_list.event_list():
            time, id1, id2, message = event[:4]
            runner.add_event(time, id1, id2, message, alert = event[4], cancel = event[5],
                             sender = event[6])

    runner.sort(file_handler.length())
    return runner


# A major reason why this function is difficult to test using unittest is simply
# because it is the final method and requires user input. On the other
# hand, all the functions inside the main() method have been tested.
def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()

    file_handler = FileHandler()
    try:
        file_handler.open_file(input_file_path)


        runner = combine_all_events_into_single_event_list(file_handler)

        for event in runner.event_list():
            logic.print_output(*event)
    except FileNotFoundError:
        print("FILE NOT FOUND")


if __name__ == '__main__':
    main()
