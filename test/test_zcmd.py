# This file is placed in the Public Domain.


"test commands"


import sys
import unittest


from opr import Cfg, Command, Handler, Object, command


evts = []
skip = ["cfg",]


param = Object()
param.cmd = [""]
param.cfg = ["nick=bot", "server=localhost", "port=6699"]
param.fnd = ["log", "log txt==test", "config", "config name=bot", "config server==localhost"]
param.flt = ["0", ""]
param.log = ["test1", "test2"]
param.mre = [""]
param.thr = [""]


class CLI(Handler):

    "test cli class"

    @staticmethod
    def raw(txt):
        if Cfg.verbose:
            sys.stdout.write(txt)
            sys.stdout.flush()


cli = CLI()


def consume(events):
    fixed = []
    res = []
    for evt in events:
        evt.wait()
        fixed.append(evt)
    for evt in fixed:
        try:
            events.remove(evt)
        except ValueError:
            continue
    return res


class TestCommands(unittest.TestCase):

    "commands test class."

    def test_commands(self):
        cmds = sorted(Command.cmd)
        for cmd in cmds:
            if cmd in skip:
                continue
            for ex in getattr(param, cmd, ""):
                evt = command(cli, cmd + " " + ex)
                evts.append(evt)
        consume(evts)
        self.assertTrue(not evts)
