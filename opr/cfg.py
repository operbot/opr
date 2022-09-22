# This file is placed in the Public Domain.


"config"


from .dft import Default


def __dir__():
    return (
            "Config",
           )


class Config(Default):

    pass
