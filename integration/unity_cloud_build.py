import re

import requests
from dotenv import load_dotenv
from smart_getenv import getenv


load_dotenv()

API_KEY = getenv('API_KEY', type=str)
ORG_ID = getenv('ORG_ID', type=str)
PROJECT_ID = getenv('PROJECT_ID', type=str)
TEMPLATE_BUILD_TARGET = getenv('TEMPLATE_BUILD_TARGET', type=str)


def api_url():
    return 'https://build-api.cloud.unity3d.com/api/v1/orgs/{}/projects/{}'.format(ORG_ID, PROJECT_ID)


def headers():
    return {'Authorization': 'Basic {}'.format(API_KEY)}


def get_build_template():
    url = '{}/buildtargets/{}'.format(api_url(), TEMPLATE_BUILD_TARGET)
    response = requests.get(url, headers=headers())

    config = response.json()
    config.pop('links')
    config.pop('buildtargetid')

    return config


def create_new_build_target(config, branch):
    name = re.sub('[^0-9a-zA-Z]+', '-', branch)

    config['name'] = 'Autobuild {}'.format(name)
    config['settings']['scm']['branch'] = branch

    url = '{}/buildtargets'.format(api_url())
    response = requests.post(url, headers=headers(), json=config)

    info = response.json()
    return info['buildtargetid']


def delete_build_target(buildtargetid):
    url = '{}/buildtargets/{}'.format(api_url(), buildtargetid)
    requests.delete(url, headers=headers())


def start_build(buildtargetid):
    url = '{}/buildtargets/{}/builds'.format(api_url(), buildtargetid)
    config = {'clean': True}
    requests.post(url, headers=headers(), json=config)


def _main():
    branch = 'feature/cloud-build-tests'

    config = get_build_template()
    buildtargetid = create_new_build_target(config, branch)
    start_build(buildtargetid)


    # delete_build_target('autobuild-feature-cloud-build-tests')


_main()
