from flask import Flask, request
import requests
from datetime import datetime
from decorator import validate
import json
import logging
import os

app = Flask(__name__)


HTTP_BAD_REQUEST_NUMBER = 400


def error_handle(endpoint='', error_msg='', status_code=400):
    res = {
        'endpoint': endpoint,
        'error_msg': error_msg,
        'status_code': status_code
    }
    logging.error('⚠️⚠️⚠️')
    logging.error(res)
    logging.error('⚠️⚠️⚠️')

    return res, status_code


def success_handle(endpoint='', data={}, status_code=200):
    res = {
        'endpoint': endpoint,
        **data
    }
    logging.info(res)

    return res, status_code


@app.route('/')
def hello():
    now = datetime.now().strftime("%H:%M:%S")
    return 'Hello World! I have been seen {} times.\n'.format(now)


@app.route('/parse', methods=['POST'])
@validate('/parse', logging)
def parse():
    try:
        endpoint = '/parse'
        question = request.get_json().get('text', '')
        res = {}

        if question:
            # url = 'http://localhost:5006/model/parse'  # @info : endpoint for another container
            # url = f"http://bot_stop_hate_core_ai:5006/model/parse"
            url = f"{os.getenv('RASA_URL')}/model/parse"
            res = requests.post(
                url,
                data=json.dumps({
                    'text': question,
                    'message_id': 'b2831e73-1407-4ba0-a861-0f30a42a2a5a'
                }),
                timeout=3000
            )
            res = res.json()
            res = {
                'intent': res.get('intent', {}),
                'entities': res.get('entities', {}),
            }
            logging.info('---------------------------------------------------------------')
            logging.info('🔥 RASA response 🔥')
            logging.info(json.dumps(res, indent=4))
            logging.info('---------------------------------------------------------------')
        else:
            return error_handle(endpoint, 'missing question', HTTP_BAD_REQUEST_NUMBER)

        return success_handle(endpoint, res)
    except Exception as e:
        return error_handle(endpoint, str(e), HTTP_BAD_REQUEST_NUMBER)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
