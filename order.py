from abc import ABC

from risk_manager import stop_loss_price_calculator, take_profit_price_calculator, margin_allocator
from platform_boundings import OandaBinding, MT5Binding
from structs import OandaOrderData, MT5OrderData, ENUM_TRADE_REQUEST_ACTIONS, ENUM_ORDER_TYPE_FILLING, ENUM_ORDER_TYPE


class Order(ABC):
    def levels_calculator(self):
        pass
    def volume_calculator(self):
        pass
    def order_data_constructor(self):
        pass
    def send_order(self):
        pass



class OandaOrder(Order):
    """
    an Oanda order object, which handles everything related to it
    """

    def create_binding(self, acc_id:str, accss_token:str):
        """
        whatever is related to server will be in the binding object
        :param acc_id: Oandas API account ID
        :param accss_token: Oanda API access token
        """
        self.binding = OandaBinding(acc_id=acc_id, accss_token=accss_token)

    def levels_calculator(self, instrument):
        """
        calculates the levels for stop-loss and take-profit
        :param order:
        :return:
        """
        current_price = self.binding.current_price_retriever(instrument)
        self.stop_loss = stop_loss_price_calculator(current_price)
        self.take_profit = take_profit_price_calculator(current_price)

    def order_data_constructor(self):
        """
        This function actually creates the order struct,
        :return:
        """
        pass

    def send_order(self):
        """
        sending the order to the server
        :param order:
        :return:
        """
        pass

class MT5Order():
    def __init__(self, direction:int, config):
        self.config = config
        self.binding = MT5Binding()
        assert direction in {0,1,-1}
        if direction == 0:
            self.direction = None
        elif direction == 1:
            self.direction = ENUM_ORDER_TYPE.ORDER_TYPE_BUY
        elif direction == -1:
            self.direction = ENUM_ORDER_TYPE.ORDER_TYPE_SELL
        else:
            raise NotImplementedError(f"the direction is {direction} but it should be 0, 1 or -1")


    def levels_calculator(self, instrument):
        current_price = self.binding.current_price_retriever(instrument)
        self.stop_loss = stop_loss_price_calculator(current_price)
        self.take_profit = take_profit_price_calculator(current_price)

    def volume_calculator(self):
        user_intended_number_of_positions = self.config.USER_INTENDED_NUMBER_OF_POSITIONS
        user_intended_symbols = self.config.USER_INTENDED_SYMBOLS
        reserved_margin_percentage = self.config.RESERVED_MARGIN_PERCENTAGE
        list_of_open_positions = self.binding.open_positions_retriever()
        account_liquidity = self.binding.account_info.account_liquidity
        allocations = margin_allocator(
            list_of_open_positions,
            user_intended_number_of_positions,
            user_intended_symbols,
            reserved_margin_percentage,
            account_liquidity
        )
        return allocations

    def order_data_constructor(self):
        self.data = []
        for instrument in self.config.INSTRUMENTS:
            self.levels_calculator(instrument)
            self.data.append(MT5OrderData(
                action=ENUM_TRADE_REQUEST_ACTIONS.TRADE_ACTION_DEAL,
                symbol=instrument,
                volume=self.volume_calculator().get("instrument"),
                sl=self.stop_loss,
                tp=self.take_profit,
                type_filling=ENUM_ORDER_TYPE_FILLING.ORDER_FILLING_IOC,
                type=self.direction
            ))

    def send_order(self):
        self.order_data_constructor()
        responses = []
        for order_data in self.data:
            responses.append(self.binding.send_order(order_data))
        return responses


