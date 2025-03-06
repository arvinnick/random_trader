from abc import ABC
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Optional
from xmlrpc.client import DateTime


class ENUM_TRADE_REQUEST_ACTIONS(Enum):
    """
    enum, including the action parameter of MT5TradeRequest:
    https:#www.mql5.com/en/docs/constants/tradingconstants/enum_trade_request_actions
    """
    TRADE_ACTION_DEAL = 1  # Place a trade order for immediate execution
    TRADE_ACTION_PENDING = 5  # Place a pending order
    TRADE_ACTION_MODIFY = 6  # Modify an existing order
    TRADE_ACTION_REMOVE = 7  # Remove an existing order
    TRADE_ACTION_CLOSE_BY = 10  # Close a position by another opposite one


class ENUM_ORDER_TYPE(Enum):
    """https:#www.mql5.com/en/docs/constants/tradingconstants/orderproperties#enum_order_type"""
    ORDER_TYPE_BUY = 0  # Market Buy order
    ORDER_TYPE_SELL = 1  # Market Sell order
    ORDER_TYPE_BUY_LIMIT = 2  # Buy Limit pending order
    ORDER_TYPE_SELL_LIMIT = 3  # Sell Limit pending order
    ORDER_TYPE_BUY_STOP = 4  # Buy Stop pending order
    ORDER_TYPE_SELL_STOP = 5  # Sell Stop pending order
    ORDER_TYPE_BUY_STOP_LIMIT = 6  # Buy Stop Limit order
    ORDER_TYPE_SELL_STOP_LIMIT = 7  # Sell Stop Limit order
    ORDER_TYPE_CLOSE_BY = 8  # OrderData to close a position by an opposite one


class ENUM_ORDER_TYPE_FILLING(Enum):
    """https://www.mql5.com/en/docs/constants/tradingconstants/orderproperties#enum_order_type"""
    ORDER_FILLING_FOK = 0  # Execute the order immediately and completely; otherwise, cancel it.
    ORDER_FILLING_IOC = 1  # Execute the order immediately with the available volume; cancel any unfilled portion.
    ORDER_FILLING_BOC = 1  #
    ORDER_FILLING_RETURN = 2  # Place the order in the queue if it cannot be filled immediately.


class ENUM_ORDER_TYPE_TIME(Enum):
    """
    https://www.mql5.com/en/docs/python_metatrader5/mt5ordercheck_py#order_type_time
    """
    ORDER_TIME_GTC = 0  # The order stays in the queue until manually canceled
    ORDER_TIME_DAY = 1  # The order is active only during the current trading day
    ORDER_TIME_SPECIFIED = 2  # The order is active until the specified date
    ORDER_TIME_SPECIFIED_DAY = 3  # The order is active until 23:59:59 of the specified day


class OrderData(ABC):
    """
    any information that is related to an order is here. Therefore, we send order objects between classes and serialize
    them accordingly
    """
    pass


@dataclass
class StopLossOnFill:
    price: str


@dataclass
class TakeProfitOnFill:
    price: str


@dataclass
class OandaOrderData(OrderData):
    type: str
    instrument: str
    units: str
    timeInForce: str
    positionFill: str
    stopLossOnFill: StopLossOnFill
    takeProfitOnFill: TakeProfitOnFill


@dataclass
class MT5OrderData(OrderData):
    """
    representation of an order of metatrader
    """
    action: ENUM_TRADE_REQUEST_ACTIONS # Trade operation type
    symbol: str  # Trade symbol
    volume: float  # Requested volume for a deal in lots
    sl: float  # Stop Loss level of the order
    tp: float  # Take Profit level of the order
    type_filling: ENUM_ORDER_TYPE_FILLING  # OrderData execution type
    type: ENUM_ORDER_TYPE  # OrderData type

    ###optional fields
    magic: Optional[int]  # Expert Advisor ID (magic number)
    order: Optional[int]  # OrderData ticket
    price: Optional[float]  # Price
    stoplimit: Optional[float]  # StopLimit level of the order
    deviation: Optional[int]  # Maximal possible deviation from the requested price
    type_time: Optional[ENUM_ORDER_TYPE_TIME]  # OrderData expiration type
    expiration: Optional[DateTime]  # OrderData expiration time (for the orders of ORDER_TIME_SPECIFIED type)
    comment: Optional[str]  # OrderData comment
    position: Optional[int]  # Position ticket
    position_by: Optional[int]  # The ticket of an opposite position


class ENUM_POSITION_TYPE(Enum):
    POSITION_TYPE_BUY: 1 #Buy
    POSITION_TYPE_SELL:0 #Sell


@dataclass
class OandaPositionData:
    pass

@dataclass
class Position:
    def serializer(self):
        return asdict(self)


@dataclass
class MT5Position(Position):
    # PositionGetString()
    POSITION_SYMBOL: str
    # PositionGetDouble()
    POSITION_VOLUME: float  # : Position volume
    POSITION_SL: float  # : Stop Loss level of opened position
    POSITION_TP: float  # : Take Profit level of opened position
    POSITION_PRICE_OPEN: Optional[float]  # : Position open price
    POSITION_PRICE_CURRENT: Optional[float]  # : Current price of the position symbol
    POSITION_SWAP: Optional[float]  # : Cumulative swap
    POSITION_PROFIT: Optional[float]  # : Current profit
    # PositionGetInteger()
    POSITION_TICKET: int
    POSITION_TYPE: ENUM_POSITION_TYPE
    @property
    def symbol(self): return self.POSITION_SYMBOL
    @property
    def volume(self): return self.POSITION_VOLUME


