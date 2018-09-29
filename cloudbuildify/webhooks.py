from flask import Flask

from cloudbuildify import config


app = Flask(__name__)


@app.route('/{}'.format(config.WEBHOOK_SECRET), methods=['POST'])
def webhook():
    return '', 200
