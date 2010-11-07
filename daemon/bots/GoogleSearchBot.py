#!/usr/bin/env python
#
# A test irc bot to do google searches and return the first 3 results.
#
# Created By Daniel Fox

import urllib
import simplejson

from base import IRCBot
from irclib.irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr



def get_results(search_query):
    query = urllib.urlencode({'q' : search_query })
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' \
      % (query)
    search_results = urllib.urlopen(url)
    json = simplejson.loads(search_results.read())
    results = json['responseData']['results']
    return results


class GoogleSearchBot(IRCBot):
    def on_pubmsg(self, c, e):
        nick = nm_to_n(e.source())
        if e.arguments()[0].startswith("search "):
            results = get_results(e.arguments()[0].split("search ", 1)[1])[:3]
            for i in range(len(results)):
                title = "Title: %s" % results[i]["titleNoFormatting"]
                self.connection.notice(nick, title.encode("utf-8", "ignore"))
                url = "URL: %s" % results[i]["url"]
                self.connection.notice(nick, url.encode("utf-8", "ignore"))

