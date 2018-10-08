import logging

import requests
from requests.auth import HTTPBasicAuth

from cloudbuildify import config


INPROGRESS = 'INPROGRESS'
SUCCESSFUL = 'SUCCESSFUL'
FAILED = 'FAILED'
STOPPED = 'STOPPED'


def api_url():
    return 'https://api.bitbucket.org/2.0/repositories/{}/{}'.format(config.BITBUCKET_ORG_ID, config.BITBUCKET_PROJECT_ID)


def build_url(commit):
    return '{}/commit/{}/statuses/build'.format(api_url(), commit)


def auth():
    return HTTPBasicAuth(config.BITBUCKET_USER, config.BITBUCKET_PASSWORD)


def set_build_status(state, key, commit, name, url):
    data = {
        'state': state,
        'key': key,
        'name': name,
        'url': url
    }
    response = requests.post(build_url(commit), auth=auth(), json=data)

    if not response.ok:
        logging.warning('Creating build target "' + data['name'] + '" failed', response.text)
