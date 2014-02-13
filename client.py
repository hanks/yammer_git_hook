#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, urllib
import json
import sys, os
import __main__

class Client(object):

    SETTINGS_FILE = 'local.settings'

    def __init__(self):
        try:
            settings_file_obj = open(os.path.dirname(__main__.__file__) + "/" + self.SETTINGS_FILE)
            data = json.load(settings_file_obj)
        except Exception, e:
            print "Read settings file error.", e
            sys.exit(1)

        self.client_id = data['client_id']
        self.request_url = data['redirect_url']
        self.msg_format = data['msg_format']
        self.target_group_list = data['target_group_list']
        self.topic_list = data['topic_list']
        self.access_token = data['access_token']

    def __str__(self):
        return u"{}-{}-{}-{}-{}".format(self.client_id, self.request_url, self.target_group_list, self.topic_list, self.access_token)

    @property
    def auth_url(self):
        return "https://www.yammer.com/dialog/oauth?client_id={}&redirect_uri={}&response_type=token".format(self.client_id, self.redirect_url)

    @property
    def profile_url(self):
        return "https://www.yammer.com/api/v1/users/current.json"

    @property
    def post_message_url(self):
        return "https://www.yammer.com/api/v1/messages.json"

    def get_group_list(self):
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
        group_list = self.get_group_list()
        for group in group_list:
            print group['group_id'],
            print group['name']

    def send_message_to_group(self, msg_part_1, msg_part_2):
        msg = self.msg_format % (msg_part_1, msg_part_2)
        for item in self.target_group_list:
            for index, topic in enumerate(self.topic_list, start=1):
                group_id = item["group_id"]
                post_data = {}
                post_data['body'] = msg.encode('utf-8')
                post_data['group_id'] = group_id
                post_data['topic{}'.format(index)] = topic['topic']

                self._do_request(self.post_message_url, post_data)
        
    def _do_request(self, url, data=None):

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
    if len(sys.argv) != 3:
        print "Argument number error, need two arguments."
        sys.exit(1)

    client = Client()
    client.send_message_to_group(sys.argv[1], sys.argv[2])
