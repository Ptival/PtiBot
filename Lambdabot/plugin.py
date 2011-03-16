###
# Copyright (c) 2011, Valentin Robert
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import string
import subprocess

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

bindir = '/home/robertv/.cabal/bin/'

class Lambdabot(callbacks.Plugin):
    """Lambdabot commands"""

    threaded = True

    def hoogle(self, irc, msg, args, num, req):
        """[<num>] <query> - Queries Hoogle.
        See http://www.haskell.org/hoogle"""
        req = string.replace(req, '`', '\`')
        cmd = bindir + 'hoogle "' + req + '" | head -' + str(num)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        msg = ''
        for line in p.stdout.readlines():
            msg += line
        for s in msg[:-1].split('\n'):
            irc.reply(s, prefixNick=False)

    hoogle = wrap(hoogle, [optional('int', 3), additional('text')])

    def kind(self, irc, msg, args, req):
        """<typevar> - Returns the kind of the type variable."""
        req = string.replace(req, '`', '\`')
        cmd = bindir + 'lambdabot -e ":kind ' + req +'"'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        msg = ''
        for line in p.stdout.readlines():
            msg += line
        for s in msg[:-1].split('\n'):
            irc.reply(s, prefixNick=False)

    kind = wrap(kind, [additional('text')])

    def pl(self, irc, msg, args, req):
        """<exp> - Applies pointless."""
        req = string.replace(req, '`', '\`')
        cmd = bindir + 'lambdabot -e ":pl ' + req +'"'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        msg = ''
        for line in p.stdout.readlines():
            msg += line
        for s in msg[:-1].split('\n'):
            irc.reply(s, prefixNick=False)

    pl = wrap(pl, [additional('text')])

    def type(self, irc, msg, args, req):
        """<exp> - Returns the type of the expression."""
        req = string.replace(req, '`', '\`')
        cmd = bindir + 'lambdabot -e ":type ' + req +'"'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()
        msg = ''
        for line in p.stdout.readlines():
            msg += line
        for s in msg[:-1].split('\n'):
            irc.reply(s, prefixNick=False)

    type = wrap(type, [additional('text')])

Class = Lambdabot


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
