# Calculate SL & TP levels. Allocate margin across intended trading position.
from __future__ import annotations

import random
from typing import Union, Any

import yaml
from flask import Flask, jsonify, Response, request

from .utils import log_handling

risk_app = Flask("risk_manager")



def stop_loss_pips_calculator(): return round(random.uniform(5, 20), 2)
def take_profit_pips_calculator(): return round(random.uniform(10, 50), 2)

CONFIG_FILE = f"{risk_app.config.root_path}/riskConfig.yaml"
with open(CONFIG_FILE) as f:
    config = yaml.safe_load(f)
if not risk_app.config.get("TESTING"):
    risk_app.config.update(config)

logger = log_handling(risk_app)


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
    return mapping.get(level).get(direction)




@risk_app.route('/risk/levels/', methods=['POST'])
def levels_calculator() -> Response:
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
    stop_loss_pips = stop_loss_pips_calculator()
    take_profit_pips = take_profit_pips_calculator()
    if take_profit_pips < 0 or stop_loss_pips < 0:
        return Response("take profit and stop loss pips cannot be negative", status=400)
    data = request.get_json()
    current_price = data.get('current_price')
    trade_direction = data.get('trade_direction')
    tp_direction = direction_interpreter(trade_direction, "take_profit")
    sl_direction = direction_interpreter(trade_direction, "stop_loss")
    if tp_direction is None or sl_direction is None:
        return Response(f"trade direction {trade_direction} is not supported", status=400)
    tp = round(float(current_price) + ((tp_direction * take_profit_pips) / 10000), 5)
    sl = round(float(current_price) + ((sl_direction * stop_loss_pips) / 10000), 5)
    risk_app.logger.info(f"Take profit and stop loss prices calculated as {tp}, {sl} for {current_price}")
    return jsonify({"take_profit": tp, "stop_loss": sl})



@risk_app.route('/risk/margin_allocator/', methods=['POST'])
def margin_allocator() -> dict[Any, Any] | Response:
    """
    Allocate margin across intended trading position. The endpoint is going to be used by a MQL4 EA. So, it doesn't take
    more than a single trading symbol.
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
            account_liquidity:
              type: number
              description: Total account liquidity
            available_margin:
              type: number
              description: Total available margin on account
    responses:
      200:
        description: Allocated margin for each symbol
        schema:
          type: object
          additionalProperties:
            type: number
    """
    reserved_margin_percentage = risk_app.config['reservedMarginPercentage']
    max_volume_per_trade = risk_app.config['maxVolumePerTrade']
    list_of_open_positions = request.json['open_positions']
    available_margin = request.json['available_margin']
    number_of_intended_position = risk_app.config['numberOfIntendedOpenPositions']
    account_liquidity = request.json['account_liquidity']
    tradable_margin = account_liquidity * (1 - reserved_margin_percentage)
    allocated_margin = round(tradable_margin / number_of_intended_position, 5)
    risk_app.logger.info(f"allocated margin is {allocated_margin} for {len(list_of_open_positions)} positions")
    remaining_margin = available_margin - (account_liquidity * reserved_margin_percentage)
    return jsonify({"allocated_margin": min([allocated_margin,
                                             max_volume_per_trade,
                                             remaining_margin])})

if __name__ == '__main__':
    risk_app.run(debug=True)