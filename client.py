#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib
import json
import sys


class Client(object):

    SETTINGS_FILE = 'local.settings'

    def __init__(self):
        pass

    def _init_settings(self):
        pass

    @property
    def auth_url(self):
        return "https://www.yammer.com/dialog/oauth?client_id={}&redirect_uri={}&response_type=token".format(self.client_id, self.redirect_url)

    @property
    def profile_url(self):
        return "https://www.yammer.com/api/v1/users/current.json"

    def get_group_id_list(self):
        pass

    def do_request(self, url, data=None):

        request = urllib2.Request(url)
        request.add_header("Authorization", "Bearer %s" % self.access_token)

        response = None
        
        if data:
            # post data should be encoded first
            data = urllib.urlencode(data)

        try:    
            response = urllib2.urlopen(request, data)
        except urllib2.HTTPError, e:
            print e.code, e.reason
            sys.exit(1)
        except Exception, e:
            print e
            sys.exit(1)
        
        return response
            
if __name__ == '__main__':
    pass
