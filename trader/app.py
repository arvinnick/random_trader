from datetime import datetime
from urllib import request
from flask import Flask,jsonify,request
import json

from order import OandaOrder, MT5Order
import yaml

from trader.platform_boundings import OandaBinding, MT5Binding

app = Flask(__name__)
logger = app.logger
with open('config.yml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    app.config.update(cfg)

@app.errorhandler(NotImplementedError)
def not_implemented(e):
    """
    error handler for anything in the request that is not implemented
    :param e: error instance
    :return: jsonified response
    """
    logger.error(e)
    return jsonify({"Not implemented": str(e)}, status_code=400)



@app.route('/trader/execute', methods=['POST'])
async def send_order(
        instrument:str = "EUR_USD"
):
    if request.method == 'POST':
        binding = request.form['binding']
        mock_request = request.form["mock"]
        if mock_request == "true":
            app.logger.info(f"This is a mock request on {datetime.now()} to make sure the scheduler is working properly")
        if binding == 'oanda':
            app.logger.info("using Oanda as the broker. No need for MetaTrader")
            order = OandaOrder()
        elif binding == 'mt4':
            app.logger.info("using MetaTrader as the binding to the broker.")
            order = MT5Order(config=app.config)
        else:
            raise NotImplementedError("only MT5 and Oanda APIs are supported, but binding is {} here".format(binding))
        response = order.send_order()
        logger.info(json.dumps(response, indent=2))




@app.route('/trader/account_data/<binding>/<parameter>', methods=['GET'])
async def server_binding(binding:str,
                         parameter:str):
    """
    this endpoints give the access to the binding data. The form can include:
    - current_price
    - available_margin
    - open_positions
    binding could be Oanda or MT5
    :return:
    """
    if binding == 'oanda':
        app.logger.info("using Oanda as the broker. No need for MetaTrader")
        acc_id = app.config["oanda_acc_id"]
        accss_token = app.config["oanda_accss_token"]
        binding = OandaBinding(acc_id, accss_token)
    elif binding == 'mt5':
        app.logger.info("using MetaTrader")
        binding = MT5Binding()
    else:
        raise NotImplementedError("only MT5 and Oanda APIs are supported")
    json_response = {}
    try:
        instrument = request.form['instrument']
    except KeyError:
        raise
    if request.form.get('current_price'):
        json_response['current_price'] = binding.current_price_retriever()
    elif request.form.get('available_margin'):
        pass
    elif request.form.get('open_positions'):
        pass
    else:
        raise NotImplementedError(f"form data should include open_positions or available_margin or current_price")



if __name__ == '__main__':
    app.run(debug=True)