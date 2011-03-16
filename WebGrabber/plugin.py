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

    def bdg(self, irc, msg, args):
        """- Grabs a joke from Blagues de geek."""
        joke = self.fetchtags(irc, 'http://www.blaguesdegeek.com/aleatoire.html',
                              'p', {'class':'contenu'}, 1)
        for l in joke[0].contents:
            if l.string:
                line = l.string.encode('utf-8')
                line = string.replace(line, '\n', '')
                line = string.replace(line, '\r', '')
                if line != '':
                    irc.reply(line, prefixNick=False)

    bdg = wrap(bdg)

    def cppdoc(self, irc, msg, args, num, req):
        """[<num>] <query> - Finds a C++ reference page (using Google)."""
        self.googleq('www.cplusplus.com/reference/', req, num, irc)

    cppdoc = wrap(cppdoc, [optional('int', 1), additional('text')])

    def google(self, irc, msg, args, num, req):
        """[<num>] <query> - Google search."""
        self.googleq('', req, num, irc)

    google = wrap(google, [optional('int', 1), additional('text')])

    def fetchtags(self, irc, req, name, attrs, num):
        try:
            website = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            irc.reply('A problem occured. Please try again.')
            return
        soup = BeautifulSoup(website,
                             convertEntities=BeautifulSoup.HTML_ENTITIES)
        tags = soup.findAll(name=name,
                            attrs=attrs,
                            limit=num)
        return tags

    def googleq(self, domain, query, num, irc):
        dict = {':':'%3A',
                '/':'%2F',
                ' ':'+'}
        domain = self.replace_all(domain, dict)
        query = self.replace_all(query, dict)
        url = ('http://www.google.com/search?q=site%3A' +
               domain + '+' + query)
        user_agent = ('Mozilla/5.0 (X11; U; Linux x86_64; en-US) ' +
        'AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 ' +
        'Safari/534.16')
        headers = {'User-Agent':user_agent,}
        request = urllib2.Request(url,None,headers)
        try:
            website = urllib2.urlopen(request)
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

    def javadoc(self, irc, msg, args, num, req):
        """[<num>] <query> - Finds a Java Doc page (using Google)."""
        self.googleq('download.oracle.com/javase/6/docs/', req, num, irc)

    javadoc = wrap(javadoc, [optional('int', 1), additional('text')])

    def lispdoc(self, irc, msg, args, num, req):
        """[<num>] <query> - Finds a Lisp Doc page (using Google)."""
        self.googleq('http://lispdoc.com/', req, num, irc)

    lispdoc = wrap(lispdoc, [optional('int', 1), additional('text')])

    def man3(self, irc, msg, args, num, req):
        """[<num>] <query> - Finds a man 3 page (using Google)."""
        self.googleq('http://linux.die.net/man/3/', req, num, irc)

    man3 = wrap(man3, [optional('int', 1), additional('text')])

    def phpdoc(self, irc, msg, args, num, req):
        """[<num>] <query> - Finds a PHP Doc page (using Google)."""
        self.googleq('http://php.net/manual/en/', req, num, irc)

    phpdoc = wrap(phpdoc, [optional('int', 1), additional('text')])

    def pythondoc(self, irc, msg, args, num, req):
        """[<num>] <query> - Finds a Python library page (using Google)."""
        self.googleq('http://docs.python.org/library/', req, num, irc)

    pythondoc = wrap(pythondoc, [optional('int', 1), additional('text')])

    def replace_all(self, text, dic):
        for i, j in dic.iteritems():
            text = text.replace(i, j)
        return text

    def savoir(self, irc, msg, args):
        """- Grabs a random statement from Savoir Inutile."""
        h2 = self.fetchtags(irc, 'http://www.savoir-inutile.com/', 'h2',
                            {'id':'phrase'}, 1)
        irc.reply(h2[0].string, prefixNick=False)

    savoir = wrap(savoir)

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
