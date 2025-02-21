from risk_manager import stop_loss_price_calculator, take_profit_price_calculator
from platform_boundings import OandaBinding
from structs import OandaOrderData


class OandaOrder:
    pass


class OandaOrder:
    """
    an Oanda order object, which handles everything related to it
    """
    def __init__(self, instrument:str):
        self.instrument = instrument

    def create_binding(self, acc_id:str, accss_token:str):
        """
        whatever is related to server will be in the binding object
        :param acc_id: Oandas API account ID
        :param accss_token: Oanda API access token
        """
        self.binding = OandaBinding(acc_id=acc_id, accss_token=accss_token)

    def stop_level_calculator(self):
        """
        calculates the levels for stop-loss and take-profit
        :param order:
        :return:
        """
        current_price = self.binding.current_price_retriever(self.instrument)
        self.stop_loss = stop_loss_price_calculator(current_price)
        self.take_profit = take_profit_price_calculator(current_price)

    def volume_calculator(self):
        """
        to get the
        :return:
        """
        #todo: write a function that gets the available margine, then the number of non-allocated instruments that you are going to trade on, then devide the available margin to them. after that you'll find out the volume you can put on the order

    def order_object_constructor(self):
        """
        This function actually creates the order struct,
        :return:
        """
        #todo: finish it after finishing the function above to fill "units". Also, use the analyzer to find the sign on units (buy or sell)
        # self.order_object = OandaOrderData(
        #     instrument=self.instrument,
        #     type= 'Market', #perhaps we will change it in the future for more advanced strategies
        #     units: str
        #     timeInForce: str
        #     positionFill: str
        #     stopLossOnFill: StopLossOnFill
        #     takeProfitOnFill: TakeProfitOnFill
        # )

    def send_order(self):
        """
        sending the order to the server
        :param order:
        :return:
        """
