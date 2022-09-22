# This file is placed in the Public Domain.


"command"


from .obj import Object


def __dir__():
    return (
            "Commands",
            "dispatch"
           )


class Command(Object):

    cmd = {}

    @staticmethod
    def add(cmd):
        Command.cmd[cmd.__name__] = cmd

    @staticmethod
    def get(cmd):
        return Command.cmd.get(cmd)

    @staticmethod
    def remove(cmd):
        del Command.cmd[cmd]


def dispatch(evt):
    evt.parse()
    func = Command.get(evt.cmd)
    if func:
        func(evt)
        evt.show()
    evt.ready()
