import thread
import traceback
import __builtin__
from whiffle import wikidotapi

thread.stack_size(1024 * 512)  # reduce vm size

class Input(dict):

    def __init__(self, conn, raw, prefix, command, params,
                 nick, user, host, paraml, msg):

        chan = paraml[0].lower()
        if chan == conn.nick.lower():  # is a PM
            chan = nick

        def say(msg):
            conn.msg(chan, msg)

        def reply(msg):
            if chan == nick:  # PMs don't need prefixes
				newmsg = msg
				if "nonick::" in msg:
					newmsg = msg.split('nonick::')[1]
				self.say(newmsg)
            else:
				if "nonick::" in msg:
					newmsg = msg.split('nonick::')[1]
					self.say(newmsg)
				else:
					self.say(nick + ': ' + msg)

        def pm(msg, nick=nick):
            conn.msg(nick, msg)

        def set_nick(nick):
            conn.set_nick(nick)

        def me(msg):
            self.say("\x01%s %s\x01" % ("ACTION", msg))

        def notice(msg):
            conn.cmd('NOTICE', [nick, msg])

        def kick(target=None, reason=None):
            conn.cmd('KICK', [chan, target or nick, reason or ''])

        def ban(target=None):
            conn.cmd('MODE', [chan, '+b', target or host])
			
			
        def unban(target=None):
            conn.cmd('MODE', [chan, '-b', target or host])

        dict.__init__(self, conn=conn, raw=raw, prefix=prefix, command=command,
                      params=params, nick=nick, user=user, host=host,
                      paraml=paraml, msg=msg, server=conn.server, chan=chan,
                      notice=notice, say=say, reply=reply, pm=pm, bot=bot,
                      kick=kick, ban=ban, unban=unban, me=me,
                      set_nick=set_nick, lastparam=paraml[-1])

    # make dict keys accessible as attributes
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


def run(func, input):
    args = func._args

    if 'inp' not in input:
        input.inp = input.paraml

    if args:
        if 'db' in args and 'db' not in input:
            input.db = get_db_connection(input.conn)
        if 'input' in args:
            input.input = input
        if 0 in args:
            out = func(input.inp, **input)
        else:
            kw = dict((key, input[key]) for key in args if key in input)
            out = func(input.inp, **kw)
    else:
        out = func(input.inp)
    if out is not None:
        input.reply(unicode(out))


def do_sieve(sieve, bot, input, func, type, args):
    try:
        return sieve(bot, input, func, type, args)
    except Exception:
        print 'sieve error',
        traceback.print_exc()
        return None


class Handler(object):

    '''Runs plugins in their own threads (ensures order)'''

    def __init__(self, func):
        self.func = func
        self.input_queue = Queue.Queue()
        thread.start_new_thread(self.start, ())

    def start(self):
        uses_db = 'db' in self.func._args
        db_conns = {}
        while True:
            input = self.input_queue.get()

            if input == StopIteration:
                break

            if uses_db:
                db = db_conns.get(input.conn)
                if db is None:
                    db = bot.get_db_connection(input.conn)
                    db_conns[input.conn] = db
                input.db = db

            try:
                run(self.func, input)
            except:
                traceback.print_exc()

    def stop(self):
        self.input_queue.put(StopIteration)

    def put(self, value):
        self.input_queue.put(value)


def dispatch(input, kind, func, args, autohelp=False):
    for sieve, in bot.plugs['sieve']:
        input = do_sieve(sieve, bot, input, func, kind, args)
        if input == None:
            return
        for mnick in blacklist_nicks:
            if input.nick.lower() == mnick.lower():
			    return

    if autohelp and args.get('autohelp', True) and not input.inp \
            and func.__doc__ is not None:
        input.reply(func.__doc__)
        return

    if hasattr(func, '_apikey'):
        key = bot.config.get('api_keys', {}).get(func._apikey, None)
        if key is None:
            input.reply('error: missing api key')
            return
        input.api_key = key

    if func._thread:
        bot.threads[func].put(input)
    else:
        thread.start_new_thread(run, (func, input))


def match_command(command):
    commands = list(bot.commands)

    # do some fuzzy matching
    prefix = filter(lambda x: x.startswith(command), commands)
    if len(prefix) == 1:
        return prefix[0]
    elif prefix and command not in prefix:
        return prefix

    return command


def main(conn, out):
    inp = Input(conn, *out)
    # EVENTS
    for func, args in bot.events[inp.command] + bot.events['*']:
        dispatch(Input(conn, *out), "event", func, args)

    if inp.command == 'PRIVMSG':
        # COMMANDS
        bot_prefix = re.escape(bot.config.get("prefix", "."))
        if inp.chan == inp.nick:  # private message, no command prefix
            prefix = r'^(?:['+bot_prefix+']?|'
        else:
            prefix = r'^(?:['+bot_prefix+']|'

        command_re = prefix + inp.conn.nick
        command_re += r'[:,]+\s+)(\w+)(?:$|\s+)(.*)'

        m = re.match(command_re, inp.lastparam)

        if m:
            trigger = m.group(1).lower()
            command = match_command(trigger)

            if isinstance(command, list):  # multiple potential matches
                input = Input(conn, *out)
                input.reply("did you mean %s or %s?" %
                            (', '.join(command[:-1]), command[-1]))
            elif command in bot.commands:
                input = Input(conn, *out)
                input.trigger = trigger
                input.inp_unstripped = m.group(2)
                input.inp = input.inp_unstripped.strip()

                func, args = bot.commands[command]
                dispatch(input, "command", func, args, autohelp=True)

        # REGEXES
        for func, args in bot.plugs['regex']:
            m = args['re'].search(inp.lastparam)
            dispatched = 0
            if m:
                input = Input(conn, *out)
                input.inp = m
                dispatched =1 
                dispatch(input, "regex", func, args)
            if dispatched == 0:
                m = args['re'].search(inp.lastparam.lower())
                if m:
                    input = Input(conn, *out)
                    input.inp = m
                    dispatch(input, "regex", func, args)

