""" A Js-like dict. Keys can be accessed both in foo["bar"] and foo.bar manner.

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
