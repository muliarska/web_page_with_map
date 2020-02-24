import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_info_by_nickname(nick):
    """
    (str) -> dict
    This function returns a dictionary with the information
    about user's friends whose nickname is a function argument.
    """
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': nick, 'count': '20'})

    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data, encoding='utf-8')
    return js
