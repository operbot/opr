README
######

**NAME**

``oper`` - write your own commands.


**SYNOPSIS**


| ``oper [-c] [-i] [-r]``
| ``oper <cmd> [key=value] [key==value]``
|

**DESCRIPTION**

``oper`` is a solid, non hackable bot, intended to be programmable in a
static, only code, no popen, fixed imports and no reading modules from a
directory, to not have a directory to read modules from to add
commands to the bot but include the own programmed modules directly into the
python code, so only trusted code (your own written code) is included and
runable. Reading random code from a directory is what gets avoided. As
experience tells os.popen and __import__, importlib are also avoided, direct
imports in the code is what is used.

``oper`` stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence. Paths carry the
type in the path name what makes reconstruction from filename easier then
reading type from the object.

``oper`` has some functionality, mostly feeding RSS feeds into a irc
channel. It can do some logging of txt and take note of things todo.
This should be the bot where you build your own one from ;]

**INSTALL**

| ``pip3 install oper --upgrade --force-reinstall``
|

**CONFIGURATION**

| configuration is done by calling the ``cfg`` command of ``oper``
| 

**irc**

| ``oper cfg server=<server> channel=<channel> nick=<nick>``
|
| (*) default channel/server is #oper on localhost
|

**sasl**

| ``oper pwd <nickservnick> <nickservpass>``
| ``oper cfg password=<outputfrompwd>``
|

**users**

| ``oper cfg users=True``
| ``oper met <userhost>``
|

**rss**

| ``oper rss <url>``
|

**RUNNING**

this part shows how to run ``oper``.

**cli**

without any arguments ``oper`` doesn't respond, add arguments to have
``oper`` execute a command:

| ``$ oper``
| ``$``
|

the ``cmd`` command shows you a list of available commands:

| ``$ oper cmd``
| ``cfg,cmd,dlt,dne,dpl,flt,fnd,ftc,log,met,mre,nme,pwd,rem,rss,tdo,thr,ver``
|

**console**

use the -c option to start the bot as a console.

| ``$ oper -c``
| ``OPERBOT started at Fri Sep 16 02:11:23 2022``
| ``> thr``
| ``Console.loop/1s``
|

**irc**

use the -i option to start the irc client.


| ``$ oper -i``
| ``OPER started at Fri Sep 16 02:11:23 2022``
| ``> cfg``
| ``server=localhost port=6667 channel=#oper nick=oper cc=!``
| ``> thr``
| ``Console.loop(8s) IRC.keep(8s) IRC.loop(8s) IRC.output(8s) thr(8s)``
| ``>`` 
|

**rss**

you can add a -r option to have the rss fetcher started.

| ``$ oper-c -r``
| ``OPER started at Fri Sep 16 02:44:51 2022``
| ``> thr``
| ``Console.loop/1s Fetcher.run/4m59s``
| ``>``
|

**COMMANDS**

here is a short description of the commands.

| ``cfg`` - show the irc configuration, also edits the config
| ``cmd`` - show all commands
| ``dlt`` - remove a user
| ``dne`` - flag todo as done
| ``dpl`` - set display items for a rss feed
| ``flt`` - show a list of bot registered to the bus
| ``fnd`` - allow you to display objects on the datastore, read-only json files on disk 
| ``ftc`` - run a rss feed fetching batch
| ``log`` - log some text
| ``met`` - add a users with there irc userhost
| ``mre`` - displays cached output, channel wise.
| ``nme`` - set name of a rss feed
| ``pwd`` - combine a nickserv name/password into a sasl password
| ``rem`` - remove a rss feed by matching is to its url
| ``rss`` - add a feed to fetch, fetcher runs every 5 minutes
| ``thr`` - show the running threads
| ``tdo`` - adds a todo item, no options returns list of todo's
| ``upt`` - show uptime
| ``ver`` - show version
|

**PROGRAMMING**

The ``op`` package provides an Object class, that mimics a dict while using
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction. Methods are
factored out into functions to have a clean namespace to read JSON data into.

basic usage is this::

>>> from op import Object
>>> o = Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> import op
>>> o = op.Object()
>>> o.key = "value"
>>> p = op.save(o)
>>> obj = op.Object()
>>> op.load(obj, p)
>>> obj.key
>>> 'value'

great for giving objects peristence by having their state stored in files::

 >>> import op
 >>> o = op.Object()
 >>> op.save(o)
 'op.obj.Object/2021-08-31/15:31:05.717063'

**AUTHOR**

Bart Thate - operbot100@gmail.com

**COPYRIGHT**

``operbot`` is placed in the Public Domain. No Copyright, No License.
