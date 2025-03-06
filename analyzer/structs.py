from enum import Enum


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