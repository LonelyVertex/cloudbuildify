import re

import requests

from cloudbuildify import config


def api_url():
    return 'https://build-api.cloud.unity3d.com/api/v1/orgs/{}/projects/{}'.format(config.ORG_ID, config.PROJECT_ID)


def headers():
    return {'Authorization': 'Basic {}'.format(config.API_KEY)}


def get_build_template():
    url = '{}/buildtargets/{}'.format(api_url(), config.TEMPLATE_BUILD_TARGET)
    response = requests.get(url, headers=headers())

    data = response.json()
    data.pop('links')
    data.pop('buildtargetid')

    return data


def create_new_build_target(data, branch):
    name = re.sub('[^0-9a-zA-Z]+', '-', branch)

    data['name'] = 'Autobuild {}'.format(name)
    data['settings']['scm']['branch'] = branch

    url = '{}/buildtargets'.format(api_url())
    response = requests.post(url, headers=headers(), json=data)

    info = response.json()
    return info['buildtargetid']


def delete_build_target(buildtargetid):
    url = '{}/buildtargets/{}'.format(api_url(), buildtargetid)
    requests.delete(url, headers=headers())


def start_build(buildtargetid):
    url = '{}/buildtargets/{}/builds'.format(api_url(), buildtargetid)
    data = {'clean': True}
    requests.post(url, headers=headers(), json=data)


def _main():
    branch = 'feature/cloud-build-tests'

    data = get_build_template()
    buildtargetid = create_new_build_target(data, branch)
    start_build(buildtargetid)


    # delete_build_target('autobuild-feature-cloud-build-tests')


_main()
