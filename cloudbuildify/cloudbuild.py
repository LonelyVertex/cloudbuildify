import logging
import re

import requests

from cloudbuildify import config


def api_url():
    return 'https://build-api.cloud.unity3d.com/api/v1/orgs/{}/projects/{}'.format(config.CLOUDBUILD_ORG_ID,
                                                                                   config.CLOUDBUILD_PROJECT_ID)


def headers():
    return {'Authorization': 'Basic {}'.format(config.CLOUDBUILD_API_KEY)}


def get_build_template():
    url = '{}/buildtargets/{}'.format(api_url(), config.CLOUDBUILD_TEMPLATE_BUILD_TARGET)
    response = requests.get(url, headers=headers())

    if not response.ok:
        logging.error('Getting build template failed', response.text)

    data = response.json()
    data.pop('links')
    data.pop('buildtargetid')

    return data


def create_new_build_target(data, branch, user):
    name_limit = 64 - 17 - len(user)
    name = re.sub('[^0-9a-zA-Z]+', '-', branch)[0:name_limit]

    data['name'] = 'Autobuild of {} by {}'.format(name, user)
    data['settings']['scm']['branch'] = branch

    url = '{}/buildtargets'.format(api_url())
    response = requests.post(url, headers=headers(), json=data)

    if not response.ok:
        logging.error('Creating build target "' + data['name'] + '" failed', response.text)

    info = response.json()
    return info['buildtargetid'], data['name']


def delete_build_target(buildtargetid):
    url = '{}/buildtargets/{}'.format(api_url(), buildtargetid)
    requests.delete(url, headers=headers())


def start_build(buildtargetid):
    url = '{}/buildtargets/{}/builds'.format(api_url(), buildtargetid)
    data = {'clean': True}
    requests.post(url, headers=headers(), json=data)


def create_build_url(buildtarget_id, build_number):
    return 'https://developer.cloud.unity3d.com/build/orgs/{}/projects/{}/buildtargets/{}/builds/{}/log/compact/'.format(
        config.CLOUDBUILD_ORG_ID, config.CLOUDBUILD_PROJECT_ID, buildtarget_id, build_number
    )
