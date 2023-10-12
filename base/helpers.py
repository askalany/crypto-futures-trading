# pylint: disable=missing-docstring
from enum import Enum, EnumType
from threading import Lock


class Singleton(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class AutoName(Enum):
    # noinspection PyMethodParameters
    def _generate_next_value_(name, start, count, last_values):
        # pylint: disable=no-self-argument
        # sourcery skip: instance-method-first-arg-name
        return name


def get_enum_type_from_member_name(key_str: str, all_enums: list[EnumType]) -> EnumType:
    enum_class_name = key_str.split(".")[0]
    for enum_class in all_enums:
        if enum_class_name == enum_class.__name__:
            return enum_class
    raise ValueError("Invalid enum")


def get_enum_member_from_name(name_str: str, all_enums: list[EnumType]) -> EnumType:
    enum_type = get_enum_type_from_member_name(name_str, all_enums)
    if enum_type is not None:
        for _, member in enum_type.__members__.items():
            if name_str == f"{member}":
                return member
    raise ValueError(f"{name_str} is not a member of {enum_type.__name__}")
