import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.pricing as pricing
import MetaTrader5 as mt5
from abc import ABC
from risk_manager import stop_loss_price_calculator, take_profit_price_calculator

class ServerBinding(ABC):
    """abstract class for server bindings"""
    def current_price_retriever(self, instrument):
        pass

    def send_order(self, instrument, units):
        pass




class Oanda(ServerBinding):
    """encapsulation of Oanda broker API"""
    def __init__(self, acc_id, accss_token):
        self.acc_id = acc_id
        self.accss_token = accss_token
        self.client = oandapyV20.API(access_token=accss_token)

    def current_price_retriever(self, instrument):
        # Get current price for stop-loss and take-profit calculation
        params = {"instruments": instrument}
        price_request = pricing.PricingInfo(self.acc_id, params=params)
        price_response = self.client.request(price_request)
        self.current_price = float(price_response["prices"][0]["bids"][0]["price"])  # Use bid price for short

    def payload_creator(self, instrument, units, stop_loss_price, take_profit_price):
        # Create Order Payload
        self.payload = {
            "order": {
                "type": "MARKET",
                "instrument": instrument,
                "units": str(units),
                "timeInForce": "FOK",
                "positionFill": "DEFAULT",
                "stopLossOnFill": {
                    "price": str(stop_loss_price)
                },
                "takeProfitOnFill": {
                    "price": str(take_profit_price)
                }
            }
        }

    def send_order(self, instrument, units):
        self.current_price_retriever(instrument)

        stop_loss_price = stop_loss_price_calculator(self.current_price)
        take_profit_price = take_profit_price_calculator(self.current_price)

        self.payload_creator(instrument, stop_loss_price, take_profit_price , units)
        # Send Order Request
        order_request = orders.OrderCreate(self.acc_id, data=self.payload)
        return self.client.request(order_request)


class MT5(ServerBinding):
    """bindings for MT5 API"""
    def __init__(self):
        if not mt5.initialize():
            print("Initialization failed")
            mt5.shutdown()
    def current_price_retriever(self, instrument):
        """retrieves the current price of the market"""
        return mt5.symbol_info_tick(instrument)

    def send_order(self, order:Order):
        """sends the order to the metatrader5"""

