# Calculate SL & TP levels
import random
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
