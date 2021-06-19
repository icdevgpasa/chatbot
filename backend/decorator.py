import functools
import json
from flask import request

HTTP_BAD_REQUEST_NUMBER = 400


def error_handle(endpoint='', error_msg='', status_code=400):
    return {
        'endpoint': endpoint,
        'error_msg': error_msg
    }, status_code


def validate(endpoint, logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # ...
                logger.info(
                    f'Request {endpoint} from {request.environ["REMOTE_ADDR"]}')
                data = request.get_json()
                logger.info(json.dumps(data, ensure_ascii=False, indent=4))

                # ...
                if data is None:
                    logger.error('Data is none !!!!')
                    return error_handle(endpoint, 'data is none', HTTP_BAD_REQUEST_NUMBER)

                return func(*args, **kwargs)
            except Exception as e:
                logger.error('⚠️validation error or BAD_REQUEST missing data!!!')
                logger.error(str(e))
                return error_handle(endpoint, 'validation error or BAD_REQUEST missing data!!!', HTTP_BAD_REQUEST_NUMBER)
        return wrapper
    return decorator
