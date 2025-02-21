# Calculate SL & TP levels
import random
from typing import List

from structs import Position

stop_loss_pips = round(random.uniform(5, 20), 2)
take_profit_pips = round(random.uniform(10, 50), 2)

def stop_loss_price_calculator(current_price:float,
                               stop_loss_pips:float = stop_loss_pips) -> float:
    """
    This is a prototype of a function that calculates the stop loss price
    :param current_price: current price in market
    :param stop_loss_pips: the number of pips below the current price
    :return: the level on which we will set the stop loss price
    """
    return round(current_price + (stop_loss_pips / 10000), 5)  # SL above entry for short

def take_profit_price_calculator(current_price:float,
                                 take_profit_pips:float = take_profit_pips) -> float:
    """
    This is a prototype of a function that calculates the take profit price
    :param current_price: current price in market
    :param take_profit_pips: the number of pips above the current price
    :return: the level on which we will set the take profit price
    """
    return round(current_price - (take_profit_pips / 10000), 5)  # TP below entry for short


def margin_allocator(list_of_open_positions:List[Position],
                     user_intended_number_of_positions:int,
                     user_intended_symbols:List[str],
                     reserved_margin_percentage:float,
                     account_liquidity:float) -> dict:
    """
    the function is a prototype of a function that calculates the margin allocation
    :param account_liquidity:
    :param reserved_margin_percentage:
    :param user_intended_symbols:
    :param list_of_open_positions:
    :param user_intended_number_of_positions: the number of positions user wants to open
    :return: dictionary, indicating how much margin is being allocated to each symbol-position
    """
    if len(list_of_open_positions) >= user_intended_number_of_positions:
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
    return {symbol: allocated_margin for symbol in iterative_list_of_symbols}

