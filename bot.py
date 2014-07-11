#!/usr/bin/env python

import os
import Queue
import sys
import traceback
import time
import __builtin__
import datetime

sys.path += ['plugins']  # so 'import hook' works without duplication 
sys.path += ['lib']
os.chdir(sys.path[0] or '.')  # do stuff relative to the install directory

# This is a throwaway variable to deal with a python bug
throwaway = datetime.datetime.strptime('20110101','%Y%m%d')
  
class Bot(object):
    def __init__(self):
        self.conns = {}
        self.persist_dir = os.path.abspath('persist')
        if not os.path.exists(self.persist_dir):
            os.mkdir(self.persist_dir)

bot = Bot()

print 'Loading plugins'

# bootstrap the reloader
eval(compile(open(os.path.join('core', 'reload.py'), 'U').read(),
             os.path.join('core', 'reload.py'), 'exec'))
reload(init=True)




print 'Connecting to IRC'

try:
    config()
    if not hasattr(bot, 'config'):
        exit()
except Exception, e:
    print 'ERROR: malformed config file:', e
    traceback.print_exc()
    sys.exit()


print 'Running main loop'

#wikidot stuff
thread.start_new_thread(cache_refresh, ())  #AUTOMATIC CACHE REFRESH HERE
thread.start_new_thread(ban_refresh, ())  #AUTOMATIC CACHE REFRESH HERE

while True:
    reload()  # these functions only do things
    config()  # if changes have occured

    for conn in bot.conns.itervalues():
        try:
            out = conn.out.get_nowait()
            main(conn, out)
        except Queue.Empty:
            pass
    while all(conn.out.empty() for conn in bot.conns.itervalues()):
        time.sleep(.1)
