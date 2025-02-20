from dataclasses import dataclass
from enum import Enum
from xmlrpc.client import DateTime


class ENUM_TRADE_REQUEST_ACTIONS(Enum):
    """
    enum, including the action parameter of MT5TradeRequest:
    https:#www.mql5.com/en/docs/constants/tradingconstants/enum_trade_request_actions
    """
    TRADE_ACTION_DEAL = 1           # Place a trade order for immediate execution
    TRADE_ACTION_PENDING = 5        # Place a pending order
    TRADE_ACTION_MODIFY = 6         # Modify an existing order
    TRADE_ACTION_REMOVE = 7         # Remove an existing order
    TRADE_ACTION_CLOSE_BY = 10      # Close a position by another opposite one

class ENUM_ORDER_TYPE(Enum):
    """https:#www.mql5.com/en/docs/constants/tradingconstants/orderproperties#enum_order_type"""
    ORDER_TYPE_BUY = 0              # Market Buy order
    ORDER_TYPE_SELL = 1             # Market Sell order
    ORDER_TYPE_BUY_LIMIT = 2        # Buy Limit pending order
    ORDER_TYPE_SELL_LIMIT = 3       # Sell Limit pending order
    ORDER_TYPE_BUY_STOP = 4         # Buy Stop pending order
    ORDER_TYPE_SELL_STOP = 5        # Sell Stop pending order
    ORDER_TYPE_BUY_STOP_LIMIT = 6   # Buy Stop Limit order
    ORDER_TYPE_SELL_STOP_LIMIT = 7  # Sell Stop Limit order
    ORDER_TYPE_CLOSE_BY = 8         # Order to close a position by an opposite one

class ENUM_ORDER_TYPE_FILLING(Enum):
    """https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties#enum_order_type"""
    ORDER_FILLING_FOK = 0  # Execute the order immediately and completely; otherwise, cancel it.
    ORDER_FILLING_IOC = 1  # Execute the order immediately with the available volume; cancel any unfilled portion.
    ORDER_FILLING_BOC = 1   #
    ORDER_FILLING_RETURN = 2  # Place the order in the queue if it cannot be filled immediately.

class ENUM_ORDER_TYPE_TIME(Enum):
    """
    https://www.mql5.com/en/docs/python_metatrader5/mt5ordercheck_py#order_type_time
    """
    ORDER_TIME_GTC = 0  # The order stays in the queue until manually canceled
    ORDER_TIME_DAY = 1  # The order is active only during the current trading day
    ORDER_TIME_SPECIFIED = 2  # The order is active until the specified date
    ORDER_TIME_SPECIFIED_DAY = 3  # The order is active until 23:59:59 of the specified day





@dataclass
class Order:
    """
    any information that is related to an order is here. Therefore, we send order objects between classes and serialize
    them accordingly
    """
    pass

@dataclass
class OandaOrder(Order):
    pass

@dataclass
class MT5Order(Order):
    """
    representation of an order of metatrader
    """
    action      :ENUM_TRADE_REQUEST_ACTIONS         # Trade operation type
    magic       :int                              # Expert Advisor ID (magic number)
    order       :int                              # Order ticket
    symbol      :str                             # Trade symbol
    volume      :float                             # Requested volume for a deal in lots
    price       :float                             # Price
    stoplimit   :float                             # StopLimit level of the order
    sl          :float                             # Stop Loss level of the order
    tp          :float                             # Take Profit level of the order
    deviation   :int                              # Maximal possible deviation from the requested price
    order_type  :ENUM_ORDER_TYPE                          # Order type
    type_filling:ENUM_ORDER_TYPE_FILLING            # Order execution type
    type_time   :ENUM_ORDER_TYPE_TIME               # Order expiration type
    expiration  :DateTime                           # Order expiration time (for the orders of ORDER_TIME_SPECIFIED type)
    comment     :str                             # Order comment
    position    :int                              # Position ticket
    position_by :int                              # The ticket of an opposite position

