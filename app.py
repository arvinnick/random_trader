from urllib import request

from flask import Flask

import json

from platform_boundings import Oanda
import yaml

app = Flask(__name__)
with open('config.yml', 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)
    app.config.update(cfg)




@app.route('trader/<units>/<instrument>', methods=['POST'])
async def send_order(
        units: int,
        instrument:str = "EUR_USD"):
    if request.method == 'POST':
        binding = request.form['binding']
        if binding == 'api':
            accss_token = app.config.get('accss_token')
            acc_id = app.config.get('acc_id')
            api = Oanda(accss_token, acc_id)
        elif binding == 'mt4':
            pass #todo: make the binding

    response = api.send_order(instrument, units)

    app.logger.info(json.dumps(response, indent=2))
