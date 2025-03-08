# Calculate SL & TP levels
import random
from typing import List, Union, Any
from flask import Flask, jsonify, Response, Request

app = Flask(__name__)



stop_loss_pips = round(random.uniform(5, 20), 2)
take_profit_pips = round(random.uniform(10, 50), 2)

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

@app.route('/risk/stop_loss/<current_price>', methods=['GET'])
def stop_loss_price_calculator(current_price:float,
                               stop_loss_pips:float = stop_loss_pips,
                               trade_direction: Union["buy","short","latheral"] = 'latheral') -> Any | None:
    """
    This is a prototype of a function that calculates the stop loss price
    :param trade_direction: the direction of the trade. used to determine the position of the stop loss price
    :param current_price: current price in market
    :param stop_loss_pips: the number of pips below the current price
    :return: the level on which we will set the stop loss price
    """
    direction = direction_interpreter(trade_direction, "stop_loss")
    sl = round(float(current_price) + (direction * (stop_loss_pips / 10000)), 5)
    app.logger.info(f"stop loss price is calculated as {sl} for {current_price}")
    return jsonify({"stop loss":sl})

@app.route('/risk/take_profit/<current_price>', methods=['GET'])
def take_profit_price_calculator(current_price:float,
                                 take_profit_pips:float = take_profit_pips,
                                 direction: Union[1,-1,0] = 0)-> Response:
    """
    This is a prototype of a function that calculates the take profit price
    :param current_price: current price in market
    :param take_profit_pips: the number of pips above the current price
    :return: the level on which we will set the take profit price
    """
    direction = direction_interpreter(direction, "take_profit")
    tp = round(float(current_price) - ((direction * take_profit_pips) / 10000), 5)
    app.logger.info(f"take profit price is calculated as {tp} for {current_price}")
    return jsonify({"take profit":tp})

@app.route('/risk/margin_allocator/', methods=['GET'])
def margin_allocator(request:Request) -> dict[Any, Any] | Response:
    """
    the function is a prototype of a function that calculates the margin allocation
    :param account_liquidity:
    :param reserved_margin_percentage:
    :param user_intended_symbols:
    :param list_of_open_positions:
    :param user_intended_number_of_positions: the number of positions user wants to open
    :return: dictionary, indicating how much margin is being allocated to each symbol-position
    """
    list_of_open_positions = request.form['open_positions']
    user_intended_number_of_positions = request.form['number_of_positions']
    user_intended_symbols = request.form['intended_symbols']
    reserved_margin_percentage = request.form['reserved_margin_percentage']
    account_liquidity = request.form['account_liquidity']
    assert user_intended_number_of_positions.isdigit(); app.logger.error(f"the number of positions is {user_intended_number_of_positions} which is not a number")
    if len(list_of_open_positions) >= int(user_intended_number_of_positions):
        return {}
    iterative_list_of_symbols =[]
    not_traded_symbols = [
        symbol for symbol in user_intended_symbols if symbol not in [
            open_position.symbol for open_position in list_of_open_positions
        ]
    ]
    random.shuffle(not_traded_symbols)
    iterative_list_of_symbols.extend(not_traded_symbols)
    for symbol in user_intended_symbols:
        if symbol not in not_traded_symbols and len(iterative_list_of_symbols) < user_intended_number_of_positions:
            iterative_list_of_symbols.append(symbol)
    tradable_margin = account_liquidity * (1 - reserved_margin_percentage)
    remaining_margin = tradable_margin - sum([position.volume for position in list_of_open_positions])
    allocated_margin = remaining_margin / len(iterative_list_of_symbols)
    return jsonify({symbol: allocated_margin for symbol in iterative_list_of_symbols})

if __name__ == '__main__':
    app.run(debug=True)