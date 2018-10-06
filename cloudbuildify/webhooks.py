import logging

from flask import Flask, request
from unidecode import unidecode

from cloudbuildify import config
from cloudbuildify.persistence import (delete_buildtargetid, get_buildtargetid,
                                       save_buildtargetid)
from cloudbuildify.unity_cloud_build import (create_new_build_target,
                                             delete_build_target,
                                             get_build_template, start_build)

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


@app.route('/{}'.format(config.WEBHOOK_SECRET), methods=['POST'])
def webhook():
    event = request.headers.get('X-Event-Key')
    branch = get_branch_name()
    user = get_user_name()

    if branch and event == 'pullrequest:created':
        pull_request_created(branch, user)
    elif branch and event in ('pullrequest:fulfilled', 'pullrequest:rejected'):
        pull_request_resolved(branch)

    return '', 200


def get_branch_name():
    data = request.get_json()
    try:
        return data['pullrequest']['source']['branch']['name']
    except (TypeError, KeyError):
        return None


def get_user_name():
    data = request.get_json()
    try:
        return unidecode(data['actor']['display_name'])
    except (TypeError, KeyError):
        return None


def pull_request_created(branch, user):
    logging.info('Creating build target for {}'.format(branch))
    template = get_build_template()
    buildtargetid = create_new_build_target(template, branch, user)
    save_buildtargetid(branch, buildtargetid)
    start_build(buildtargetid)


def pull_request_resolved(branch):
    logging.info('Deleting build target for {}'.format(branch))
    buildtargetid = get_buildtargetid(branch)
    delete_build_target(buildtargetid)
    delete_buildtargetid(branch)
