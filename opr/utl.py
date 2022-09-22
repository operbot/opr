# This file is placed in the Public Domain.


"utiltity"


import os
import pathlib
import time


def __dir__():
    return (
            "cdir",
            "elapsed",
            "fns",
            "fntime",
            "fnclass",
            "spl",
            "wait"
           )


def cdir(path):
    if os.path.exists(path):
        return
    if os.sep in path:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
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
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt


def fns(path, timed=None):
    if not path:
        return []
    if not os.path.exists(path):
        return []
    res = []
    for rootdir, dirs, _files in os.walk(path, topdown=False):
        for dname in  dirs:
            ddd = os.path.join(rootdir, dname)
            fls = sorted(os.listdir(ddd))
            if fls:
                opath = os.path.join(ddd, fls[-1])
                if (
                    timed
                    and "from" in timed
                    and timed["from"]
                    and fntime(opath) < timed["from"]
                   ):
                    continue
                if timed and timed.to and fntime(opath) > timed.to:
                    continue
                try:
                    fntime(opath)
                except ValueError:
                    continue
                opath = opath.split("store")[-1][1:]
                res.append(opath)
    return sorted(res, key=fntime)


def fntime(path):
    after = 0
    path = " ".join(path.split(os.sep)[-2:])
    if "." in path:
        path, after = path.rsplit(".")
    tme = time.mktime(time.strptime(path, "%Y-%m-%d %H:%M:%S"))
    if after:
        try:
            tme = tme + float(".%s"% after)
        except ValueError:
            pass
    return tme


def fnclass(path):
    pth = []
    try:
        _rest, *pth = path.split("store")
    except ValueError:
        pass
    if not pth:
        pth = path.split(os.sep)
    return pth[0]


def spl(txt):
    try:
        res = txt.split(",")
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


def wait():
    while 1:
        time.sleep(1.0)
