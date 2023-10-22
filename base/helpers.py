from enum import Enum


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AutoName(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        # sourcery skip: instance-method-first-arg-name
        return name
