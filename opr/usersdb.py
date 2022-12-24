# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402,R0903


"users"


import time


from .objects import Class, Object, find, fntime, match, save, update, write
from .threads import elapsed


def __dir__():
    return (
            "dlt",
            "met",
            "opr"
           )


class NoUser(Exception):

    pass

class Users(Object):

    @staticmethod
    def allowed(origin, perm):
        perm = perm.upper()
        user = Users.get_user(origin)
        val = False
        if user and perm in user.perms:
            val = True
        return val

    @staticmethod
    def delete(origin, perm):
        res = False
        for user in Users.get_users(origin):
            try:
                user.perms.remove(perm)
                save(user)
                res = True
            except ValueError:
                pass
        return res

    @staticmethod
    def get_users(origin=""):
        selector = {"user": origin}
        return find("user", selector)

    @staticmethod
    def get_user(origin):
        users = list(Users.get_users(origin))
        res = None
        if len(users) > 0:
            res = users[-1]
        return res

    @staticmethod
    def perm(origin, permission):
        user = Users.get_user(origin)
        if not user:
            raise NoUser(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            save(user)
        return user


class User(Object):

    def __init__(self, val=None):
        super().__init__()
        self.user = ""
        self.perms = []
        if val:
            update(self, val)


Class.add(User)


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
    event.done()


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
    user = match("mod.irc.User", {"user": event.rest})
    if not user:
        user = User()
    user.user = event.rest
    if "OPER" not in user.perms:
        user.perms.append("OPER")
    write(user)
    event.done()
