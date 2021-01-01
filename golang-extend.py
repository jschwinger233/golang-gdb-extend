import gdb


class Cast(gdb.Function):

    def __init__(self):
        super().__init__('cast')

    def invoke(self, obj: gdb.Value, type: gdb.Value) -> gdb.Value:
        # address casting
        if obj.type.name == 'long':
            return cast_address(obj, type.string())

        # interface casting
        elif obj.type.name == '':
            return cast_interface(obj, '')

        else:
            raise ValueError('object type not supported')


def cast_address(obj: gdb.Value, type: str) -> gdb.Value:
    gdb_type = gdb.lookup_type(type).pointer()
    return obj.cast(gdb_type)


Cast()
