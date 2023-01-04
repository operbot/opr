# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402,E1101


"enable/disable modules"


from genocide import Cfg, edit, keys, last, printable, write


def __dir__():
    return (
            "dis",
            "ena",
            "krn"
           )

def krn(event):
    last(Cfg)
    if not event.sets:
        event.reply(printable(
                              Cfg,
                              keys(Cfg),
                              skip="name,password,prs",
                             )
                   )
    else:
        edit(Cfg, event.sets)
        write(Cfg)
        event.ok()


def dis(event):
    if not event.args:
        event.reply("dis <modname>")
        return
    name = event.args[0]
    if name == "krn":
        event.reply("i won't disable myself")
        return
    Cfg.mod.replace(name, "")
    Cfg.mod.replace(",,", ",")
    write(Cfg)
    event.ok()


def ena(event):
    if not event.args:
        event.reply("ena <modname>")
        return
    Cfg.mod += ",%s" % event.args[0]
    write(Cfg)
    event.ok()
