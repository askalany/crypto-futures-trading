from enum import Enum


class AutoName(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        # sourcery skip: instance-method-first-arg-name
        return name
