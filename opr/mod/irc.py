# This file is placed in the Public Domain.


"internet relay chat"


import base64
import os
import queue
import random
import socket
import ssl
import textwrap
import threading
import time
import _thread


from opr import Callbacks, Class, Client, Default, Event, Object
from opr import edit, elapsed, keys, printable, save, update
from opr import find, fntime, locked, last, launch


def __dir__():
    return (
        "Config",
        "Event",
        "IRC",
        "DCC",
        "init",
        "cfg",
        "dlt",
        "met",
        "mre",
        "pwd"
    )


def init():
    i = IRC()
    launch(i.start)
    return i


saylock = _thread.allocate_lock()


class NoUser(Exception):

    pass


class Config(Default):

    channel = ""
    control = "!"
    nick = ""
    password = ""
    port = 6667
    realname = ""
    sasl = False
    server = "localhost"
    servermodes = ""
    sleep = 60
    username = ""
    users = False

    def __init__(self):
        super().__init__()
        self.control = Config.control
        self.channel = Config.channel
        self.nick = Config.nick 
        self.password = Config.password
        self.port = Config.port
        self.realname = Config.realname
        self.sasl = Config.sasl
        self.server = Config.server
        self.servermodes = Config.servermodes
        self.sleep = Config.sleep
        self.username = Config.username
        self.users = Config.users


Class.add(Config)


class IrcEvent(Event):

    def __init__(self):
        Event.__init__(self)
        self.args = []
        self.arguments = []
        self.channel = ""
        self.command = ""
        self.nick = ""
        self.origin = ""
        self.rawstr = ""
        self.sock = None
        self.type = "event"
        self.txt = ""


class TextWrap(textwrap.TextWrapper):

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = True
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 450


class Output(Object):

    cache = Object()

    def __init__(self):
        Object.__init__(self)
        self.oqueue = queue.Queue()
        self.dostop = threading.Event()

    def dosay(self, channel, txt):
        raise NotImplementedError

    def extend(self, channel, txtlist):
        if channel not in self.cache:
            self.cache[channel] = []
        self.cache[channel].extend(txtlist)

    def get(self, channel):
        value = None
        try:
            value = self.cache[channel].pop(0)
        except IndexError:
            pass
        return value

    def oput(self, channel, txt):
        self.oqueue.put_nowait((channel, txt))

    def output(self):
        while not self.dostop.isSet():
            (channel, txt) = self.oqueue.get()
            if channel is None and txt is None:
                break
            if self.dostop.isSet():
                break
            wrapper = TextWrap()
            txtlist = wrapper.wrap(txt)
            if len(txtlist) > 3:
                self.extend(channel, txtlist)
                self.dosay(channel, "%s put in cache, use !mre to show more" % len(txtlist))
                continue
            _nr = -1
            for txt in txtlist:
                _nr += 1
                self.dosay(channel, txt)

    def size(self, name):
        if name in self.cache:
            return len(self.cache[name])
        return 0

    def start(self):
        self.dostop.clear()
        launch(self.output)
        return self

    def stop(self):
        self.dostop.set()
        self.oqueue.put_nowait((None, None))


class IRC(Client, Output):

    def __init__(self):
        Client.__init__(self)
        Output.__init__(self)
        self.buffer = []
        self.cfg = Config()
        self.connected = threading.Event()
        self.channels = []
        self.joined = threading.Event()
        self.keeprunning = False
        self.outqueue = queue.Queue()
        self.sock = None
        self.speed = "slow"
        self.state = Object()
        self.state.needconnect = False
        self.state.error = ""
        self.state.last = 0
        self.state.lastline = ""
        self.state.nrconnect = 0
        self.state.nrerror = 0
        self.state.nrsend = 0
        self.state.pongcheck = False
        self.threaded = False
        self.zelf = ""
        self.register("903", cb_h903)
        self.register("904", cb_h903)
        self.register("AUTHENTICATE", cb_auth)
        self.register("CAP", cb_cap)
        self.register("ERROR", cb_error)
        self.register("LOG", cb_log)
        self.register("NOTICE", cb_notice)
        self.register("PRIVMSG", cb_privmsg)
        self.register("QUIT", cb_quit)

    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt)

    @locked(saylock)
    def command(self, cmd, *args):
        if not args:
            self.raw(cmd)
        elif len(args) == 1:
            self.raw("%s %s" % (cmd.upper(), args[0]))
        elif len(args) == 2:
            self.raw("%s %s :%s" % (cmd.upper(), args[0], " ".join(args[1:])))
        elif len(args) >= 3:
            self.raw(
                "%s %s %s :%s" % (cmd.upper(),
                                  args[0],
                                  args[1],
                                  " ".join(args[2:]))
            )
        if (time.time() - self.state.last) < 4.0:
            time.sleep(4.0)
        self.state.last = time.time()

    def connect(self, server, port=6667):
        self.state.nrconnect += 1
        self.connected.clear()
        if self.cfg.password:
            self.cfg.sasl = True
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
            ctx.check_hostname = False
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = ctx.wrap_socket(sock)
            self.sock.connect((server, port))
            self.raw("CAP LS 302")
        else:
            addr = socket.getaddrinfo(server, port, socket.AF_INET)[-1][-1]
            self.sock = socket.create_connection(addr)
        if self.sock:
            os.set_inheritable(self.fileno(), os.O_RDWR)
            self.sock.setblocking(True)
            self.sock.settimeout(180.0)
            self.connected.set()
            return True
        return False

    def disconnect(self):
        self.sock.shutdown(2)

    def doconnect(self, server, nck, port=6667):
        while 1:
            try:
                if self.connect(server, port):
                    break
            except (OSError, ConnectionResetError) as ex:
                self.state.error = str(ex)
            time.sleep(self.cfg.sleep)
        self.logon(server, nck)

    def dosay(self, channel, txt):
        self.joined.wait()
        txt = str(txt).replace("\n", "")
        txt = txt.replace("  ", " ")
        self.command("PRIVMSG", channel, txt)

    def event(self, txt):
        evt = self.parsing(txt)
        cmd = evt.command
        if cmd == "PING":
            self.state.pongcheck = True
            self.command("PONG", evt.txt or "")
        elif cmd == "PONG":
            self.state.pongcheck = False
        if cmd == "001":
            self.state.needconnect = False
            if self.cfg.servermodes:
                self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
            self.zelf = evt.args[-1]
            self.joinall()
        elif cmd == "002":
            self.state.host = evt.args[2][:-1]
        elif cmd == "366":
            self.state.error = ""
            self.joined.set()
        elif cmd == "433":
            self.state.error = txt
            nck = self.cfg.nick + "_" + str(random.randint(1,10))
            self.command("NICK", nck)
        return evt

    def fileno(self):
        return self.sock.fileno()

    def joinall(self):
        for channel in self.channels:
            self.command("JOIN", channel)

    def keep(self):
        while 1:
            self.connected.wait()
            self.keeprunning = True
            time.sleep(self.cfg.sleep)
            self.state.pongcheck = True
            self.command("PING", self.cfg.server)
            time.sleep(10.0)
            if self.state.pongcheck:
                self.keeprunning = False
                self.restart()

    def logon(self, server, nck):
        assert server
        assert nck
        assert self.cfg.username
        assert self.cfg.realname
        self.raw("NICK %s" % nck)
        self.raw(
                 "USER %s %s %s :%s" % (self.cfg.username,
                 server,
                 server,
                 self.cfg.realname)
                )

    def parsing(self, txt):
        rawstr = str(txt)
        rawstr = rawstr.replace("\u0001", "")
        rawstr = rawstr.replace("\001", "")
        obj = IrcEvent()
        obj.rawstr = rawstr
        obj.command = ""
        obj.arguments = []
        arguments = rawstr.split()
        if arguments:
            obj.origin = arguments[0]
        else:
            obj.origin = self.cfg.server
        if obj.origin.startswith(":"):
            obj.origin = obj.origin[1:]
            if len(arguments) > 1:
                obj.command = arguments[1]
                obj.type = obj.command
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.count(":") <= 1 and arg.startswith(":"):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        obj.arguments.append(arg)
                obj.txt = " ".join(txtlist)
        else:
            obj.command = obj.origin
            obj.origin = self.cfg.server
        try:
            obj.nick, obj.origin = obj.origin.split("!")
        except ValueError:
            obj.nick = ""
        target = ""
        if obj.arguments:
            target = obj.arguments[0]
        if target.startswith("#"):
            obj.channel = target
        else:
            obj.channel = obj.nick
        if not obj.txt:
            obj.txt = rawstr.split(":", 2)[-1]
        if not obj.txt and len(arguments) == 1:
            obj.txt = arguments[1]
        spl = obj.txt.split()
        if len(spl) > 1:
            obj.args = spl[1:]
        obj.type = obj.command
        obj.orig = repr(self)
        obj.txt = obj.txt.strip()
        return obj

    def poll(self):
        self.connected.wait()
        if not self.buffer:
            try:
                self.some()
            except (socket.timeout, ConnectionResetError) as ex:
                self.joined.clear()
                time.sleep(5.0)
                evt = IrcEvent()
                evt.txt = str(ex)
                evt.type = "ERROR"
                evt.orig = repr(self)
                return evt
        return self.event(self.buffer.pop(0))

    def raw(self, txt):
        txt = txt.rstrip()
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        txt += "\n"
        txt = bytes(txt, "utf-8")
        if self.sock:
            try:
                self.sock.send(txt)
            except (ConnectionResetError, BrokenPipeError) as ex:
                time.sleep(5.0)
                self.state.error = str(ex)
                self.stop()
        self.state.last = time.time()
        self.state.nrsend += 1

    def reconnect(self):
        try:
            self.disconnect()
        except OSError:
            pass
        self.connected.clear()
        self.joined.clear()
        self.doconnect(self.cfg.server, self.cfg.nick, int(self.cfg.port))

    def register(self, typ, cbs):
        Callbacks.add(typ, cbs)

    def say(self, channel, txt):
        self.oput(channel, txt)

    def some(self):
        self.connected.wait()
        if not self.sock:
            return
        inbytes = self.sock.recv(512)
        txt = str(inbytes, "utf-8")
        if txt == "":
            raise ConnectionResetError
        self.state.lastline += txt
        splitted = self.state.lastline.split("\r\n")
        for line in splitted[:-1]:
            self.buffer.append(line)
        self.state.lastline = splitted[-1]

    def start(self):
        assert self.cfg.nick
        assert self.cfg.server
        last(self.cfg)
        if self.cfg.channel not in self.channels:
            self.channels.append(self.cfg.channel)
        self.connected.clear()
        self.joined.clear()
        Output.start(self)
        Client.start(self)
        launch(
               self.doconnect,
               self.cfg.server,
               self.cfg.nick, int(self.cfg.port or "6667")
              )
        if not self.keeprunning:
            launch(self.keep)

    def stop(self):
        try:
            self.sock.shutdown(2)
        except OSError:
            pass
        Client.stop(self)
        #Output.stop(self)

    def wait(self):
        self.joined.wait()


def cb_auth(event):
    time.sleep(1.0)
    bot = event.bot()
    bot.raw("AUTHENTICATE %s" % bot.cfg.password)


def cb_cap(event):
    time.sleep(1.0)
    bot = event.bot()
    if bot.cfg.password and "ACK" in event.arguments:
        bot.raw("AUTHENTICATE PLAIN")
    else:
        bot.raw("CAP REQ :sasl")


def cb_h903(event):
    time.sleep(1.0)
    bot = event.bot()
    bot.raw("CAP END")


def cb_h904(event):
    time.sleep(1.0)
    bot = event.bot()
    bot.raw("CAP END")


def cb_error(event):
    bot = event.bot()
    bot.state.nrerror += 1
    #bot.state.error = event.txt
    bot.stop()


def cb_kill(event):
    pass


def cb_log(event):
    pass


def cb_notice(event):
    bot = event.bot()
    if event.txt.startswith("VERSION"):
        txt = "\001VERSION %s %s - %s\001" % (
            "op",
            bot.cfg.version,
            bot.cfg.username,
        )
        bot.command("NOTICE", event.channel, txt)


def cb_privmsg(event):
    event.parse()
    if event.txt:
        bot = event.bot()
        if event.txt[0] in [bot.cfg.cc, "!"]:
            event.txt = event.txt[1:]
        elif event.txt.startswith("%s:" % bot.cfg.nick):
            event.txt = event.txt[len(bot.cfg.nick)+1:]
        else:
            return
        if bot.cfg.users and not Users.allowed(event.origin, "USER"):
            return
        splitted = event.txt.split()
        splitted[0] = splitted[0].lower()
        event.txt = " ".join(splitted)
        event.type = "event"
        bot.handle(event)


def cb_quit(event):
    bot = event.bot()
    if event.orig and event.orig in bot.zelf:
        bot.reconnect()


class User(Object):

    def __init__(self, val=None):
        super().__init__()
        self.user = ""
        self.perms = []
        if val:
            update(self, val)


Class.add(User)


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
            res = users[-1][-1]
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


def cfg(event):
    config = Config()
    last(config)
    if not event.sets:
        event.reply(printable(
                              config,
                              keys(config),
                              skip="control,password,realname,sleep,username")
                             )
    else:
        edit(config, event.sets)
        save(config)
        event.reply("ok")


def dlt(event):
    if not event.args:
        event.reply("dlt <username>")
        return
    selector = {"user": event.args[0]}
    for _fn, obj in find("user", selector):
        obj.__deleted__ = True
        save(obj)
        event.reply("ok")
        break


def met(event):
    if not event.rest:
        _nr = 0
        for _fn, obj in find("user"):
            event.reply("%s %s %s %s" % (
                                         _nr,
                                         obj.user,
                                         obj.perms,
                                         elapsed(time.time() - fntime(_fn)))
                                        )
            _nr += 1
        return
    user = User()
    user.user = event.rest
    user.perms = ["USER"]
    save(user)
    event.reply("ok")


def mre(event):
    if not event.channel:
        event.reply("channel is not set.")
        return
    bot = event.bot()
    if "cache" not in dir(bot):
        event.reply("bot is missing cache")
        return
    if event.channel not in bot.cache:
        event.reply("no output in %s cache." % event.channel)
        return
    for _x in range(3):
        txt = bot.get(event.channel)
        if txt:
            bot.say(event.channel, txt)
    size = bot.size(event.channel)
    event.reply("%s more in cache" % size)


def pwd(event):
    if len(event.args) != 2:
        event.reply("pwd <nick> <password>")
        return
    txt = "\x00%s\x00%s" % (event.args[0], event.args[1])
    enc = txt.encode("ascii")
    base = base64.b64encode(enc)
    dcd = base.decode("ascii")
    event.reply(dcd)
