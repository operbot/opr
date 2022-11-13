# This file is placed in the Public Domain.
# pylint: disable=R,C,W,C0302


"utility"


## import


import getpass
import os
import pwd
import time
import types


from stat import ST_UID, ST_MODE, S_IMODE


## define


def __dir__():
    return (
            'debian',
            'elapsed',
            'filesize',
            'locked',
            'permission',
            'spl',
            'touch',
            'user',
            'wait'
           ) 


__all__ = __dir__()


## utility


def debian():
    return os.path.isfile("/etc/debian_version")


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt.strip()
    if hours:
        txt += "%sh" % hours
    if minutes:
        txt += "%sm" % minutes
    if sec:
        txt += "%ss" % sec
    txt = txt.strip()
    return txt


def filesize(path):
    return os.stat(path)[6]


def locked(lock):

    noargs = False

    def lockeddec(func, *args, **kwargs):

        def lockedfunc(*args, **kwargs):
            lock.acquire()
            if args or kwargs:
                locked.noargs = True
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                lock.release()
            return res

        lockeddec.__wrapped__ = func
        lockeddec.__doc__ = func.__doc__
        return lockedfunc

    return lockeddec


def permission(ddir, username, group=None, umode=0o700):
    group = group or username
    try:
        pwdline = pwd.getpwnam(username)
        uid = pwdline.pw_uid
        gid = pwdline.pw_gid
    except KeyError:
        uid = os.getuid()
        gid = os.getgid()
    stats = os.stat(ddir)
    if stats[ST_UID] != uid:
        os.chown(ddir, uid, gid)
    if S_IMODE(stats[ST_MODE]) != umode:
        os.chmod(ddir, umode)
    return True


def spl(txt):
    try:
        res = txt.split(",")
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


def touch(fname):
    fd = os.open(fname, os.O_WRONLY | os.O_CREAT)
    os.close(fd)


def user():
    try:
        return getpass.getuser() 
    except ImportError:
        return ""


def wait():
    while 1:
        time.sleep(1.0)
