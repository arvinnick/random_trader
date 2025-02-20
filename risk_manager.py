# Calculate SL & TP levels
import random
stop_loss_pips = round(random.uniform(5, 20), 2)
take_profit_pips = round(random.uniform(10, 50), 2)

def stop_loss_price_calculator(current_price, stop_loss_pips = stop_loss_pips): return round(current_price + (stop_loss_pips / 10000), 5)  # SL above entry for short
def take_profit_price_calculator(current_price, take_profit_pips = take_profit_pips): return round(current_price - (take_profit_pips / 10000), 5)  # TP below entry for short
