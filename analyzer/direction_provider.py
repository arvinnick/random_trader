
import random

import yaml
from flask import Flask

from structs import ENUM_ORDER_TYPE

app = Flask(__name__)

logger = app.logger

@app.route('analyzer/direction', methods=['GET'])
def get_direction():
    direction = random.choice([0, 1, -1])
    assert direction in {0, 1, -1}
    if direction == 0:
        return None
    elif direction == 1:
        return ENUM_ORDER_TYPE.ORDER_TYPE_BUY
    elif direction == -1:
        return ENUM_ORDER_TYPE.ORDER_TYPE_SELL
    else:
        raise NotImplementedError(f"the direction is {direction} but it should be 0, 1 or -1")