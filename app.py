from urllib import request
from flask import Flask
import json
from order import OandaOrder, MT5Order
import yaml


app = Flask(__name__)
logger = app.logger
with open('config.yml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    app.config.update(cfg)




@app.route('trader/execute', methods=['POST'])
async def send_order(
        instrument:str = "EUR_USD"
):
    if request.method == 'POST':
        binding = request.form['binding']
        if binding == 'api':
            order = OandaOrder()
        elif binding == 'mt4':
            order = MT5Order()
        else:
            raise NotImplementedError("only MT5 and Oanda APIs are supported, but binding is {} here".format(binding))
        response = order.send_order()
        logger.info(json.dumps(response, indent=2))
