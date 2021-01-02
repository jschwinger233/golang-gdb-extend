import gdb
from enum import Enum


class GDBValueType(Enum):
    UNKNOWN = 0
    INTERFACE = 1
    ADDRESS = 2
    VOID_POINTER = 3


def cast_address(obj: gdb.Value, type: str) -> gdb.Value:
    gdb_type = gdb.lookup_type(type).pointer()
    return obj.cast(gdb_type)


def cast_interface(obj: gdb.Value, type: str) -> gdb.Value:
    gdb_type = gdb.lookup_type(type)
    return obj.cast(gdb_type)


class Cast(gdb.Function):
    _dispatch = {
        GDBValueType.ADDRESS: cast_address,
        GDBValueType.INTERFACE: cast_interface,
        GDBValueType.VOID_POINTER: cast_address,
    }

    def __init__(self):
        super().__init__('cast')

    def invoke(self, obj: gdb.Value, type: gdb.Value) -> gdb.Value:
        try:
            type_string = type.string()
        except gdb.error:
            raise gdb.error('the second argument must be literal string')

        try:
            dispatch = self._dispatch[parse_type(obj)]
        except KeyError:
            raise gdb.error(
                'the first argument must be of supported types: interface, literal address, void*'
            )

        return dispatch(obj, type_string)


def parse_type(obj: gdb.Value) -> GDBValueType:
    try:
        if str(obj['tab'].type) == 'runtime.itab *':
            return GDBValueType.INTERFACE
    except:
        if obj.type.name == 'long':
            return GDBValueType.ADDRESS
        elif str(obj.type) == 'void *':
            return GDBValueType.VOID_POINTER
        else:
            return GDBValueType.UNKNOWN


Cast()
