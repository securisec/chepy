class StateNotList(Exception):  # pragma: no cover
    def __init__(self, msg="State is not a list", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class StateNotDict(Exception):  # pragma: no cover
    def __init__(self, msg="State is not a dict", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
