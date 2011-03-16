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
import urllib2
from BeautifulSoup import BeautifulSoup

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks


class WebGrabber(callbacks.Plugin):
    """Grabs random stuff from the internetz!"""
    threaded = True

    def google(self, domain, query):
        dict = {':':'%3A',
                '/':'%2F',
                ' ':'+'}
        domain = self.replace_all(domain, dict)
        query = self.replace_all(query, dict)
        url = ('http://www.google.com/search?q=site%3A' +
               domain + '+' + query)
        user_agent = ('Mozilla/5.0 (X11; U; Linux x86_64; en-US)' +
        'AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133' +
        'Safari/534.16')
        headers = {'User-Agent':user_agent,}
        request = urllib2.Request(url,None,headers)
        website = urllib2.urlopen(request)
        return website

    def javadoc(self, irc, msg, args, num, req):
        """[<num>] <query> - Finds a Java Doc page."""
        try:
            website = self.google('download.oracle.com/javase/6/docs/', req)
        except urllib2.HTTPError, e:
            irc.reply('A problem occured. Please try again.')
            return
        soup = BeautifulSoup(website,
                             convertEntities=BeautifulSoup.HTML_ENTITIES)
        sites = soup.findAll(name='h3',
                             attrs={'class':'r'},
                             limit=num)
        for s in sites:
            url = s.contents[0]['href']
            irc.reply(url)

    javadoc = wrap(javadoc, [optional('int', 1), additional('text')])

    def replace_all(self, text, dic):
        for i, j in dic.iteritems():
            text = text.replace(i, j)
        return text

    def urbandic(self, irc, msg, args):
        """- Grabs a random Urban Dictionary definition."""
        url = 'http://www.urbandictionary.com/random.php'
        try:
            website = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            irc.reply('A problem occured. Please try again.')
            return
        soup = BeautifulSoup(website,
                             convertEntities=BeautifulSoup.HTML_ENTITIES)
        td_word = soup.findAll(name='td',
                               attrs={'class':'word'},
                               limit=1)
        div_def = soup.findAll(name='div',
                               attrs={'class':'definition'},
                               limit=1)
        for t in td_word:
            word = string.replace(t.string, '\n', '')
            irc.reply('Word: ' + word, prefixNick=False)
        defn = ''
        for d in div_def:
            for c in d.contents:
                if c.string:
                    defn += c.string
        irc.reply('Def.: ' + defn, prefixNick=False)

    urbandic = wrap(urbandic)

Class = WebGrabber


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
