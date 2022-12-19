# This file is placed in the Public Domain.
# pylint: disable=R0903,C0115,C0116,W0212


"mailbox"


import mailbox
import os
import time


from opr.obj import Class, Object, find, fntime, printable, save
from opr.thr import elapsed


def __dir__():
    return (
            "Email",
            "cor",
            "eml",
            "mbx"
           )


bdmonths = [
            'Bo',
            'Jan',
            'Feb',
            'Mar',
            'Apr',
            'May',
            'Jun',
            'Jul',
            'Aug',
            'Sep',
            'Oct',
            'Nov',
            'Dec'
           ]


monthint = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}


class Email(Object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""


Class.add(Email)


def to_date(date):
    date = date.replace("_", ":")
    res = date.split()
    ddd = ""
    try:
        if "+" in res[3]:
            raise ValueError
        if "-" in res[3]:
            raise ValueError
        int(res[3])
        ddd = "{:4}-{:#02}-{:#02} {:6}".format(res[3], monthint[res[2]], int(res[1]), res[4])
    except (IndexError, KeyError, ValueError) as ex:
        try:
            if "+" in res[4]:
                raise ValueError from ex
            if "-" in res[4]:
                raise ValueError from ex
            int(res[4])
            ddd = "{:4}-{:#02}-{:02} {:6}".format(res[4], monthint[res[1]], int(res[2]), res[3])
        except (IndexError, KeyError, ValueError):
            try:
                ddd = "{:4}-{:#02}-{:02} {:6}".format(res[2], monthint[res[1]], int(res[0]), res[3])
            except (IndexError, KeyError):
                try:
                    ddd = "{:4}-{:#02}-{:02}".format(res[2], monthint[res[1]], int(res[0]))
                except (IndexError, KeyError):
                    try:
                        ddd = "{:4}-{:#02}".format(res[2], monthint[res[1]])
                    except (IndexError, KeyError):
                        try:
                            ddd = "{:4}".format(res[2])
                        except (IndexError, KeyError):
                            ddd = ""
    return ddd


def cor(event):
    if not event.args:
        event.reply("cor <email>")
        return
    _nr = -1
    for _fn, email in find("email", {"From": event.args[0]}):
        _nr += 1
        txt = ""
        if len(event.args) > 1:
            txt = ",".join(event.args[1:])
        else:
            txt = "From,Subject"
        event.reply("%s %s %s" % (
                                  _nr,
                                  printable(email, txt, plain=True),
                                  elapsed(time.time() - fntime(email.__stp__)))
                                 )


def eml(event):
    if not event.args:
        event.reply("eml <searchtxtinemail>")
        return
    _nr = -1
    for obj in find("email"):
        if event.rest in obj.text:
            _nr += 1
            event.reply("%s %s %s" % (
                                      _nr,
                                      printable(obj, "From,Subject"),
                                      elapsed(time.time() - fntime(obj.__fnm__)))
                                     )


def mbx(event):
    if not event.args:
        event.reply("mbx <directory>")
        return
    fnm = os.path.expanduser(event.args[0])
    event.reply("reading from %s" % fnm)
    nmr = 0
    if os.path.isdir(fnm):
        thing = mailbox.Maildir(fnm, create=False)
    elif os.path.isfile(fnm):
        thing = mailbox.mbox(fnm, create=False)
    else:
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    for ema in thing:
        email = Email(ema._headers)
        email.text = ""
        for payload in ema.walk():
            if payload.get_content_type() == 'text/plain':
                email.text += payload.get_payload()
        email.text = email.text.replace("\\n", "\n")
        save(email)
        nmr += 1
    if nmr:
        event.reply("ok %s" % nmr)
