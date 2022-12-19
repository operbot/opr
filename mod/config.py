# This file is placed in the Public Domain


"config"


from opr.objects import last, printable, keys, edit, write
from opr.running import Cfg


def __dir__():
    return (
            "cfg",
            "disable",
            "enable"
           ) 


def cfg(event):
    last(Cfg)
    if not event.sets:
        event.reply(printable(
                              Cfg,
                              keys(Cfg),
                             )
                   )
    else:
        edit(Cfg, event.sets)
        write(Cfg)
        event.done()


def disable(event):
    if not event.args:
        event.reply("disable <modname>")
        return
    name = event.args[0]
    if name == "disable":
        event.reply("i won't disable myself")
        return
    Cfg.mod.replace(name, "")
    Cfg.mod.replace(",,", ",")
    write(Cfg)
    event.ok()


def enable(event):
    if not event.args:
        event.reply("enable <modname>")
        return
    name = event.args[0]
    if name == "enable":
        event.reply("i won't enable myself")
        return
    Cfg.mod += ",name"
    write(Cfg)
    event.ok(newpath)
