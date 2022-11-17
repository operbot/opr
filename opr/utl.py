# This file is placed in the Public Domain.
# pylint: disable=R,C,W,C0302


"utility"


import getpass
import os
import pwd
import time
import traceback
import types


from stat import ST_UID, ST_MODE, S_IMODE


def __dir__():
    return (
            'debian',
            'elapsed',
            'filesize',
            'spl',
            'touch',
            'user',
            'wait'
           ) 


__all__ = __dir__()


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
