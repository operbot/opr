# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402,R0903


"users"


from .objects import Class, Object, find, save, update


def __dir__():
    return (
            "Users",
            "User"
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
