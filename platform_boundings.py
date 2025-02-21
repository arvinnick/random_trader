from dataclasses import asdict
from oandapyV20.endpoints import pricing, accounts, positions


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
    def available_margin_retriever(self):
        pass
    def open_positions_retriever(self):
        pass




class OandaBinding(ServerBinding):
    """encapsulation of Oanda broker API"""
    def __init__(self, acc_id, accss_token):
        self.acc_id = acc_id
        self.accss_token = accss_token
        self.client = oandapyV20.API(access_token=accss_token)
        self.account_summary_endpoint = accounts.AccountSummary(acc_id)

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

    def available_margin_retriever(self) -> float:
        """
        the function sends a request to client to retrieve the available margin
        :return: float, the available margin in Oanda account
        """
        try:
            # Make the API request
            response = self.client.request(self.account_summary_endpoint)

            # Extract available margin (balance for trading)
            available_margin = response['account']['marginAvailable']

            return float(available_margin)

        except Exception as e:
            raise e

    def open_positions_retriever(self):
        """
        gets all the open positions
        """
        req = positions.OpenPositions(self.acc_id)
        res = self.client.request(req)
        return res #todo: not tested due to Oanda new account restrictions




class MT5Binding(ServerBinding):
    """bindings for MT5Binding API"""
    def __init__(self):
        if not mt5.initialize():
            print("Initialization failed")
            mt5.shutdown()
        self.account_info = mt5.account_info()
    def current_price_retriever(self, instrument):
        """retrieves the current price of the market"""
        return mt5.symbol_info_tick(instrument)

    def send_order(self, order:MT5OrderData):
        """sends the order to the metatrader5"""
        self.order_serializer(order)
        result = mt5.order_send(asdict(order))
        return result.retcode
    def available_margin_retriever(self):
        """
        the function sends a request to client to retrieve the available margin
        :return: float, available margin in MT5 account
        """
        # Extract available margin
        return float(self.account_info.margin_free)

    def open_positions_retriever(self):
        """
        gets all the open positions
        """
        return mt5.positions_get()

