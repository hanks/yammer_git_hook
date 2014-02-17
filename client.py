#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib
import json
import sys, os
import __main__
from optparse import OptionParser

class Client(object):

    SETTINGS_FILE = 'local.settings'

    def __init__(self):
        try:
            settings_file_obj = open(os.path.dirname(__main__.__file__) + "/" + self.SETTINGS_FILE)
            data = json.load(settings_file_obj)
        except Exception, e:
            print "Read settings file error.", e
            sys.exit(1)
        try:
            self.client_id = data['client_id']
            self.request_url = data['redirect_url']
            self.msg_format = data['msg_format']
            self.target_group_list = data['target_group_list']
            self.topic_list = data['topic_list']
            self.access_token = data['access_token']
        except:
            print "sorry for my hard coding with security considirations."
            print "json data is not valid!!"
            sys.exit(1)

    def __str__(self):
        return u"{}-{}-{}-{}-{}".format(self.client_id, self.request_url, self.target_group_list, self.topic_list, self.access_token)

    @property
    def auth_url(self):
        """return auth url from cliend_id and redirect_url

        copy it to browser, do auth and get access_token from redirect_url
        """
        return "https://www.yammer.com/dialog/oauth?client_id={}&redirect_uri={}&response_type=token".format(self.client_id, self.redirect_url)

    @property
    def profile_url(self):
        """Yammer REST API, to get self profile info
        """
        return "https://www.yammer.com/api/v1/users/current.json"

    @property
    def post_message_url(self):
        """Yammer REST API, to send message
        """
        return "https://www.yammer.com/api/v1/messages.json"

    def get_group_list(self):
        """Get group info list from profile_url above
        """
        response = self._do_request(self.profile_url)
        json_data = json.loads(response.read())
        group_list = []
        for item in json_data['web_preferences']['home_tabs']:
            if item['type'] == 'group':
                temp_dict = {}
                temp_dict['group_id'] = item['group_id']
                temp_dict['name'] = item['name']
                group_list.append(temp_dict)
        return group_list

    def print_group_list(self):
        """Simple print group list info
        """
        group_list = self.get_group_list()
        for group in group_list:
            print group['group_id'],
            print group['name']

    def send_message_to_group(self, msg):
        """Build POST data to send message with post_message_url
        """
        for item in self.target_group_list:
            for index, topic in enumerate(self.topic_list, start=1):
                group_id = item["group_id"]
                post_data = {}
                post_data['body'] = msg.encode('utf-8')
                post_data['group_id'] = group_id
                post_data['topic{}'.format(index)] = topic['topic']

                self._do_request(self.post_message_url, post_data)
        
    def _do_request(self, url, data=None):
        """Use urllib2 to send post request with auth header
        """
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
    # get args from command line
    usage = """
usage: %prog [-g] msg_part_1 msg_part_2
"""
    parser = OptionParser(usage)
    parser.add_option("-g", action="store_true", dest="print_group", help="print group info list")

    (options, args) = parser.parse_args()
    
    if len(sys.argv) > 3:
        parser.error("Argument number error!! At most two arguments!!")

    client = Client()

    if options.print_group:
        client.print_group_list()
    else:
        msg = client.msg_format % (msg_part_1, msg_part_2)
        client.send_message_to_group(msg)
