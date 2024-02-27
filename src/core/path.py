from functools import wraps
from pathlib import Path


def path_converter(cls):
    original_init = cls.__init__

    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        new_kwargs = {k: (Path(v) if k.endswith('_path') and isinstance(v, str) else v) for k, v in kwargs.items()}
        original_init(self, *args, **new_kwargs)

    cls.__init__ = new_init
    return cls
