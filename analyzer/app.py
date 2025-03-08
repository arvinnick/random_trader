
import random
from dataclasses import asdict

from flask import Flask, jsonify

from structs import ENUM_ORDER_TYPE

app = Flask(__name__)

logger = app.logger

def response_builder(direction):
    status = 200
    return jsonify({
        "direction": direction,
        "status": status
    })

@app.route('/analyzer/direction', methods=['GET'])
def get_direction():
    direction = random.choice([0, 1, -1])
    assert direction in {0, 1, -1}
    if direction == 0:
        logger.info("direction is latherl")
        return response_builder(None)
    elif direction == 1:
        return response_builder(ENUM_ORDER_TYPE.ORDER_TYPE_BUY.value)
    elif direction == -1:
        logger.info("direction is sell")
        return response_builder(ENUM_ORDER_TYPE.ORDER_TYPE_SELL.value)
    else:
        logger.error(f"direction is {direction} which is not supported")
        raise NotImplementedError(f"the direction is {direction} but it should be 0, 1 or -1")