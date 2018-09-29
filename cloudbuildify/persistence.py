import redis

from cloudbuildify import config

r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT)


def save_buildtargetid(branch, buildtargetid):
    r.set(branch, buildtargetid)


def get_buildtargetid(branch):
    buildtargetid = r.get(branch)
    return buildtargetid.decode() if buildtargetid else None


def delete_buildtargetid(branch):
    r.delete(branch)
