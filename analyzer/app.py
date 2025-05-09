
import random

from flask import Flask, jsonify, request

from .structs import ENUM_ORDER_TYPE
from .utils import log_handling

analyze_app = Flask("analyzer")


logger = log_handling(analyze_app)

def response_builder(direction):
    status = 200
    return jsonify({
        "direction": direction,
        "status": status
    })

@analyze_app.route('/analyzer/direction/', methods=['POST'])
def get_direction():
    form_data = request.get_json()
    currency_pair = form_data.get('currency_pair')
    direction = random.choice([0, 1, -1])
    assert direction in {0, 1, -1}
    if direction == 0:
        logger.info("direction is lateral")
        return response_builder(None)
    elif direction == 1:
        return response_builder(ENUM_ORDER_TYPE.ORDER_TYPE_BUY.value)
    elif direction == -1:
        logger.info("direction is sell")
        return response_builder(ENUM_ORDER_TYPE.ORDER_TYPE_SELL.value)
    else:
        logger.error(f"direction is {direction} which is not supported")
        raise NotImplementedError(f"the direction is {direction} but it should be 0, 1 or -1")