import flask_restful as restful
from functools import wraps
from flask import request
import time
from .Flask_app import app, app_logger


def role_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        method_name = func.__name__
        http_method = request.method
        endpoint = request.endpoint or "Unknown"
        remote_addr = request.remote_addr or "Unknown"
        app_logger.info(f"=== RESOURCE CALL START ===")
        app_logger.info(f"Method: {http_method} {method_name}")
        app_logger.info(f"Endpoint: {endpoint}")
        try:
            result = func(*args, **kwargs)
            execution_time = round((time.time() - start_time) * 1000, 2)  # in milliseconds

            app_logger.info(f"=== RESOURCE CALL SUCCESS ===")
            app_logger.info(f"Method: {http_method} {method_name}")
            app_logger.info(f"Execution Time: {execution_time}ms")

            if isinstance(result, dict):
                errCode = result.get('errCode', 'Unknown')
                message = result.get('msg', 'No message')
                app_logger.info(f"Response - ErrorCode: {errCode}, Message: {message}")
            else:
                result_type = type(result).__name__
                app_logger.info(f"Response type: {result_type}")

            app_logger.info(f"=== RESOURCE CALL END ===")
            return result

        except Exception as e:
            execution_time = round((time.time() - start_time) * 1000, 2)
            error_msg = str(e)
            error_type = type(e).__name__
            error_module = e.__class__.__module__

            app_logger.error(f"=== RESOURCE ERROR OCCURRED ===")
            app_logger.error(f"Method: {http_method} {method_name}")
            app_logger.error(f"Error Type: {error_type}")
            app_logger.error(f"Error Module: {error_module}")
            app_logger.error(f"Error Message: {error_msg}")
            app_logger.error(f"Execution Time: {execution_time}ms")
            app_logger.error(f"Client IP: {remote_addr}")

            return {
                'errCode': 1,
                'msg': f'Error in Resource {method_name}:{error_msg}',
                'error_type': error_type,
                'error_module': error_module,
                'execution_time_ms': execution_time,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                'resource_info': {
                    'method': method_name,
                    'http_method': http_method,
                    'endpoint': endpoint
                }
            }

    return wrapper

class Resource(restful.Resource):
    method_decorators = [log_decorator, role_decorator]

