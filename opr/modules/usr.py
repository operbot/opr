# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402


"user commands"


import time


from .. import User, elapsed, find, fntime, match, save, write


def dlt(event):
    if not event.args:
        event.reply("dlt <username>")
        return
    selector = {"user": event.args[0]}
    for obj in find("user", selector):
        obj.__deleted__ = True
        save(obj)
        event.done()
        break


def met(event):
    if not event.rest:
        nmr = 0
        for obj in find("user"):
            event.reply("%s %s %s %s" % (
                                         nmr,
                                         obj.user,
                                         obj.perms,
                                         elapsed(time.time() - fntime(obj.__fnm__)))
                                        )
            nmr += 1
        return
    user = User()
    user.user = event.rest
    user.perms = ["USER"]
    save(user)
    event.ok()


def opr(event):
    if not event.rest:
        nmr = 0
        for obj in find("user"):
            event.reply("%s %s %s %s" % (
                                         nmr,
                                         obj.user,
                                         obj.perms,
                                         elapsed(time.time() - fntime(obj.__fnm__)))
                                        )
            nmr += 1
        return
    user = match("user", {"user": event.rest})
    if not user:
        user = User()
    user.user = event.rest
    if "OPER" not in user.perms:
        user.perms.append("OPER")
    write(user)
    event.done()
