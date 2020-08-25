import os
import yaml

from .models import Config
from .models import RequestAuth

def _read_yaml_file(filename, cls):
    core_dire = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(core_dire,'..', filename)
    with open(file_path, mode='r', encoding='UTF-8') as file:
        config = yaml.load(file)
        return cls(**config)


def read_config():
    try:
        return _read_yaml_file('config.yaml', Config)
    except IOError as e:
        print("""Error:couldn't file the configuration file
        config.yaml  on your current directory
         Default format is:',
        consumer_key: '<gG6nDe5FtCRNVxnjSO76EVMIc>'        
        consumer_secret: '<UrkmvknW5U5l3SuReq1c5zZrAxzcGBYUiVNlQAkbBcxK4IOCaz>'        
        request_token_url: 'https://api.twitter.com/oauth/request_token'        
        access_token_url:  'https://api.twitter.com/oauth/access_token'        
        authorize_url: 'https://api.twitter.com/oauth/authorize'        
        api_version: '1.1'        
        search_endpoint: 'https://api.twitter.com/1.1/search/tweets.json'
        """)
        raise

def read_reqauth():
    try:
        return _read_yaml_file('.twitterauth', RequestAuth)
    except IOError as e:
        print(('It seems you have  not authorised your application. Please run auth.py first'))
