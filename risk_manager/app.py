# Calculate SL & TP levels
from __future__ import annotations

import random
from typing import Union, Any

import yaml
from flask import Flask, jsonify, Response, request

app = Flask(__name__)



stop_loss_pips = round(random.uniform(5, 20), 2)
take_profit_pips = round(random.uniform(10, 50), 2)

CONFIG_FILE = "config.yaml"

def direction_interpreter(direction: Union["buy","short","latheral"],
                          level:Union["take_profit", "stop_loss"]) -> int:
    mapping = {
        'take_profit':{
            "buy":1, "short":-1, "latheral":0
        },
        'stop_loss':{
            "buy":-1, "short":1, "latheral":0
        }
    }
    return mapping[level][direction]

def config_loader(config_file:str) -> dict[Any, Any]:
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config


@app.route('/risk/levels/', methods=['POST'])
def levels_calculator(take_profit_pips: float = take_profit_pips,
                      stop_loss_pips: float = stop_loss_pips) -> Response:
    """
    Calculate the take profit and stop loss prices based on current price and trade direction.
    ---
    parameters:
      - name: current_price
        in: formData
        type: number
        required: true
        description: Current market price.
      - name: trade_direction
        in: formData
        type: string
        required: true
        enum: ["buy", "short", "latheral"]
        description: Trade direction ("buy", "short", or "latheral").
      - name: take_profit_pips
        in: formData
        type: number
        required: false
        description: Number of pips for take profit. (Optional, defaults to random)
      - name: stop_loss_pips
        in: formData
        type: number
        required: false
        description: Number of pips for stop loss. (Optional, defaults to random)
    responses:
      200:
        description: Take profit and stop loss prices calculated successfully.
        schema:
          type: object
          properties:
            take_profit:
              type: number
              example: 1.23456
            stop_loss:
              type: number
              example: 1.23300
    """
    current_price = request.form.get('current_price')
    trade_direction = request.form.get('trade_direction')
    tp_direction = direction_interpreter(trade_direction, "take_profit")
    sl_direction = direction_interpreter(trade_direction, "stop_loss")
    tp = round(float(current_price) - ((tp_direction * take_profit_pips) / 10000), 5)
    sl = round(float(current_price) - ((sl_direction * stop_loss_pips) / 10000), 5)
    app.logger.info(f"Take profit and stop loss prices calculated as {tp}, {sl} for {current_price}")
    return jsonify({"take_profit": tp, "stop_loss": sl})



@app.route('/risk/margin_allocator/', methods=['POST'])
def margin_allocator() -> dict[Any, Any] | Response:
    """
    Allocate margin across intended trading positions.
    ---
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            open_positions:
              type: array
              items:
                type: object
                properties:
                  symbol:
                    type: string
                  volume:
                    type: number
            account_liquidity:
              type: number
              description: Total account liquidity
    responses:
      200:
        description: Allocated margin for each symbol
        schema:
          type: object
          additionalProperties:
            type: number
    """
    config = config_loader(CONFIG_FILE)
    reserved_margin_percentage = config['reservedMarginPercentage']
    list_of_open_positions = request.json['open_positions']
    account_liquidity = request.json['account_liquidity']
    tradable_margin = account_liquidity * (1 - reserved_margin_percentage)
    remaining_margin = tradable_margin - sum([position.volume for position in list_of_open_positions])
    allocated_margin = round(remaining_margin / len(list_of_open_positions), 5)
    app.logger.info(f"allocated margin is {allocated_margin} for {len(list_of_open_positions)} positions")
    return jsonify({"allocated_margin": allocated_margin})

if __name__ == '__main__':
    app.run(debug=True)