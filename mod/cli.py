# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0411,C0413


"command line interface"


from opr import Cfg, Client, command


class CLI(Client):

    def announce(self, txt):
        pass

    def raw(self, txt):
        print(txt)


def init():
    cli = CLI()
    command(cli, Cfg.otxt)
