from dataclasses import asdict
import oandapyV20.endpoints.pricing as pricing

import oandapyV20
import oandapyV20.endpoints.orders as orders
import MetaTrader5 as mt5
from abc import ABC
from structs import OrderData, OandaOrderData, MT5OrderData


class ServerBinding(ABC):
    """abstract class for server bindings"""

    def send_order(self, order: OrderData):
        pass
    def current_price_retriever(self, instrument:str):
        pass




class OandaBinding(ServerBinding):
    """encapsulation of Oanda broker API"""
    def __init__(self, acc_id, accss_token):
        self.acc_id = acc_id
        self.accss_token = accss_token
        self.client = oandapyV20.API(access_token=accss_token)

    def current_price_retriever(self, instrument:str):
        """Get current price for stop-loss and take-profit calculation"""
        params = {"instruments": instrument}
        price_request = pricing.PricingInfo(self.acc_id, params=params)
        price_response = self.client.request(price_request)
        return float(price_response["prices"][0]["bids"][0]["price"])  # Use bid price for short


    def send_order(self, order:OandaOrderData):
        self.current_price_retriever(order.instrument)
        order_payload = {"order": asdict(order)}
        # Send OrderData Request
        order_request = orders.OrderCreate(self.acc_id, data=order_payload)
        return self.client.request(order_request)


class MT5Binding(ServerBinding):
    """bindings for MT5Binding API"""
    def __init__(self):
        if not mt5.initialize():
            print("Initialization failed")
            mt5.shutdown()
    def current_price_retriever(self, instrument):
        """retrieves the current price of the market"""
        return mt5.symbol_info_tick(instrument)

    def send_order(self, order:MT5OrderData):
        """sends the order to the metatrader5"""
        self.order_serializer(order)
        result = mt5.order_send(asdict(order))
        return result.retcode



