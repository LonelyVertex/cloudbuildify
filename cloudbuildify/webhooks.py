import logging

from flask import Flask, request
from unidecode import unidecode

from cloudbuildify import bitbucket
from cloudbuildify import cloudbuild
from cloudbuildify import config
from cloudbuildify.persistence import BuildTarget

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
app = Flask(__name__)


@app.route('/bitbucket/{}'.format(config.BITBUCKET_WEBHOOK_SECRET), methods=['POST'])
def bitbucket_webhook():
    event = request.headers.get('X-Event-Key')
    args = get_pull_request_args()

    if args and event == 'pullrequest:created':
        pull_request_created(*args)
    elif args and event in ('pullrequest:fulfilled', 'pullrequest:rejected'):
        pull_request_resolved(*args)
    elif args and event == 'pullrequest:updated':
        pull_request_updated(*args)

    return '', 200


@app.route('/cloudbuild/{}'.format(config.CLOUDBUILD_WEBHOOK_SECRET), methods=['POST'])
def cloudbuild_webhook():
    event = request.headers.get('X-UnityCloudBuild-Event')

    if event == 'ProjectBuildQueued':
        build_status_updated(bitbucket.INPROGRESS)
    elif event == 'ProjectBuildSuccess':
        build_status_updated(bitbucket.SUCCESSFUL)
    elif event == 'ProjectBuildFailure':
        build_status_updated(bitbucket.FAILED)
    elif event == 'ProjectBuildCanceled':
        build_status_updated(bitbucket.STOPPED)

    return '', 200


def get_pull_request_args():
    data = request.get_json()
    try:
        branch = data['pullrequest']['source']['branch']['name']
        commit = data['pullrequest']['source']['commit']['hash']
        user_name = unidecode(data['actor']['display_name'])
        return branch, commit, user_name
    except (TypeError, KeyError):
        return None


def pull_request_created(branch, commit, user):
    logging.info('Creating build target for {}'.format(branch))
    template = cloudbuild.get_build_template()
    buildtarget_id, buildtarget_name = cloudbuild.create_new_build_target(template, branch, user)
    BuildTarget.create(branch, commit, buildtarget_id, buildtarget_name)
    cloudbuild.start_build(buildtarget_id)


def pull_request_updated(branch, commit, _user):
    logging.info('Updating head for {}'.format(branch))
    buildtarget = BuildTarget.find(git_branch=branch)
    buildtarget.git_commit = commit
    buildtarget.save()


def pull_request_resolved(branch, _commit, _user):
    logging.info('Deleting build target for {}'.format(branch))
    buildtarget = BuildTarget.find(git_branch=branch)
    cloudbuild.delete_build_target(buildtarget.buildtarget_id)
    buildtarget.delete()


def build_status_updated(state):
    data = request.get_json()
    buildtarget_name = data['buildTargetName']
    build_number = data['buildNumber']
    buildtarget = BuildTarget.find(buildtarget_name=buildtarget_name)

    if not buildtarget:
        return

    logging.info('Updating build status for {} to {}'.format(buildtarget_name, state))
    key = '{}-{}'.format(buildtarget.buildtarget_id[:35], build_number)
    url = cloudbuild.create_build_url(buildtarget.buildtarget_id, build_number)

    bitbucket.set_build_status(state, key, buildtarget.git_commit, buildtarget.buildtarget_name, url)
