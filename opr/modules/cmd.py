# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402


"list of commands"


from .. import Command


def __dir__():
    return (
            'cmd',
           )


def cmd(event):
    event.reply(",".join(sorted(Command.cmd)))
