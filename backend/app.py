from flask import Flask, request
import requests
from datetime import datetime
from decorator import validate
import json
import logging
import os
from os import environ
import hashlib
import pymongo
import copy
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

HTTP_BAD_REQUEST_NUMBER = 400


# DB .....
client = pymongo.MongoClient(
    host=os.environ['MONGODB_HOSTNAME'],
    port=int(os.environ['MONGODB_PORT']),
    username=os.environ['MONGODB_USERNAME'],
    password=os.environ['MONGODB_PASSWORD'],
)

db_name = 'chatbot'
container_cache_name = 'cache'
db = client[db_name]
col_cache = db[container_cache_name]


# Func .....
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


def proccess_data(data=[]):
    try:
        res = []
        for d in data:
            message = d.get('text', '').lower().lstrip().rstrip()
            message = ' '.join(message.split())
            if message:
                res.append({
                    'text': d.get('text', ''),
                    'id': d.get('id', ''),
                    'message': message,
                    'hash': hashlib.md5(message.encode()).hexdigest()
                })
        return res
    except Exception as e:
        logging.error('proccess_data(...)')
        logging.error(e)
        return data


def save_to_cache(data):
    try:
        col_cache.insert_one(data)
    except Exception as e:
        logging.info('save_to_cache()')
        logging.info(e)


def Average(lst):
    return sum(lst) / len(lst)


def hate_or_not(data):
    try:
        threshold = 0.70
        pos_intent = ['mood_great']
        minus_intent = ['mood_great', 'mood_unhappy', 'insults',
                        'religion', 'drugs', 'hateSpeech', 'suicide']
        minus_entity = ['hate_ent', 'suicide_ent', 'drugs_ent']

        top_intent = data.get('intent', {})
        top_intent_name = top_intent.get('name', '')
        top_intent_confidence = top_intent.get('confidence', 0)
        entities = data.get('entities', [])

        if not top_intent:
            print('[0]')
            return {'hate_status': False}

        if not top_intent and (len(entities) < 1):
            print('[0]')
            return {'hate_status': False}

        if (top_intent_name in pos_intent) and (top_intent_confidence >= threshold) and (len(entities) < 1):
            print('[1]')
            return {'hate_status': False}

        if (top_intent_name in pos_intent) and (len(entities) > 0):
            print('[2]')
            confidence = [e.get('confidence_entity', 0) for e in entities]
            confidence.append(top_intent_confidence)
            confidence = Average(confidence)
            return {'hate_status': confidence > threshold}

        if (top_intent_name in minus_intent) and (len(entities) > 0):
            print('[3]')
            confidence = [e.get('confidence_entity', 0) for e in entities]
            confidence.append(top_intent_confidence)
            confidence = Average(confidence)
            return {'hate_status': confidence > threshold}

        if (top_intent_name in minus_intent) and (top_intent_confidence >= threshold) and (len(entities) < 1):
            print('[4]')
            return {'hate_status': True}

        return {'hate_status': True}
    except Exception as e:
        logging.error('hate_or_not(...)')
        logging.error(res)
        return {'hate_status': False}

# ROUTES .....


def ask_rasa(question):
    try:
        # url = 'http://localhost:5006/model/parse'  # @info : endpoint for another container
        # url = f"http://bot_stop_hate_core_ai:5006/model/parse"
        # url = f"{os.getenv('RASA_URL')}/model/parse"
        url = 'http://hejt.ml/rasa/model/parse'
        url = 'https://hejt.ml/rasa/model/parse'

        res = requests.post(
            url,
            data=json.dumps({
                'text': question,
                'message_id': hashlib.md5(question.encode()).hexdigest()
            }),
            # 'message_id' : 'b2831e73-1407-4ba0-a861-0f30a42a2a5a'
            timeout=3000
        )
        res = res.json()
        res = {
            'question': question,
            'intent': res.get('intent', {}),
            'entities': res.get('entities', {}),
            'intent_ranking': res.get('intent_ranking', {}),
            'status': True,
            **hate_or_not(res)
        }

        logging.info('----------------------------------------------------')
        logging.info('🔥 RASA response 🔥')
        logging.info(json.dumps(res, indent=4))
        logging.info('----------------------------------------------------')

        return res
    except Exception as e:
        logging.error('ask_rasa(...)')
        logging.error(res)
        return {
            'error_msg': 'rasa has problem',
            'rasa_error': str(e),
            'question': question,
            'intent': {},
            'entities': {},
            'status': False,
            'hate_status': False
        }


@app.route('/')
def hello():
    now = datetime.now().strftime("%H:%M:%S")
    return 'Hello World! I have been seen {} times.\n'.format(now)


@app.route('/parse', methods=['POST'])
@validate('/parse', logging)
def parse():
    try:
        endpoint = '/parse'
        res = {}

        messages_ = proccess_data([
            {
                'text': request.get_json().get('text', ''),
                'id': request.get_json().get('id', ''),
            }
        ])
        messages_hash = messages_[0].get('hash', '')
        res_ = col_cache.find_one(
            {'hash': messages_hash},
            {'_id': 0}
        )

        # ...
        if res_:
            d = hate_or_not(res_)
            res_['hate_status']  = d['hate_status']
            logging.info('RESPONSE FROM DB')
            logging.info(res_)
            return success_handle(endpoint, {**res_, 'DB_STATUS': True})

        # ...
        question = request.get_json().get('text', '')
        if question:
            res = ask_rasa(question)
            to_db = {**messages_[0], **res}
            col_cache.insert_one(to_db)
        else:
            return error_handle(endpoint, 'missing question', HTTP_BAD_REQUEST_NUMBER)

        return success_handle(endpoint, res)
    except Exception as e:
        return error_handle(endpoint, str(e), HTTP_BAD_REQUEST_NUMBER)


@app.route('/handle_messages', methods=['POST'])
@validate('/handle_messages', logging)
def handle_messages():
    try:
        endpoint = '/handle_messages'
        logging.info(request.get_json())
        messages = request.get_json().get('messages', [])

        messages_ = proccess_data(messages)
        res_finall = []

        for data in messages_:
            question = data.get('message', '')
            if question:
                res_ = ask_rasa(question)
                if res_.get('status', False):
                    to_db = {**data, **res_}
                    res_finall.append(copy.deepcopy(to_db))
                    save_to_cache(to_db)

        return success_handle(endpoint, {'messages': res_finall})
    except Exception as e:
        return error_handle(endpoint, str(e), HTTP_BAD_REQUEST_NUMBER)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
