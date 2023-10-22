from enum import EnumType


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
