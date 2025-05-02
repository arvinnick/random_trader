import requests
import yaml, logging
from flask import Flask, request, jsonify

trader_app = Flask("trader")

def log_handling(app: Flask):
    logger = app.logger
    # Set the logger level (you can use DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logger.setLevel(logging.INFO)
    # Create a file handler
    file_handler = logging.FileHandler(f'{app.name}.log')
    file_handler.setLevel(logging.INFO)
    # Create a log format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    # Add the file handler to the app logger
    logger.addHandler(file_handler)
    return logger

CONFIG_FILE = f"{trader_app.config.root_path}/config.yml"
with open(CONFIG_FILE) as f:
    config = yaml.safe_load(f)
if not trader_app.config.get("TESTING"):
    trader_app.config.update(config)

logger = log_handling(trader_app)




@trader_app.route('/', methods=['POST'])
def trade_endpoint():
    payload = request.get_json()
    request_identifier = payload.get("request_identifier")
    for key in ["current_price", "currency_pair", "open_positions",
                "account_liquidity", "available_margin", "request_identifier"]:
        if key not in payload:
            logger.error(f"missing key {key} in payload")
            return jsonify(message=f"missing key {key} in payload", status=400)
        if key == "open_positions":
            for position in payload.get("open_positions"):
                for key in ["symbol", "volume"]:
                    if key not in position:
                        logger.error(f"missing key {key} in open positions")
                        return jsonify(message=f"missing key {key} in one of the open positions",
                                       status=400)

    #analyze
    currency_pair = payload.get("currency_pair")
    analyze_endpoints = trader_app.config.get("analyzer").get("endpoints")
    analyzer_host = trader_app.config.get("analyzer").get("host")
    port = trader_app.config.get("analyzer").get("port")
    direction_endpoint = analyze_endpoints.get("direction").get("endpoint")
    url = f"http://{analyzer_host}:{port}{direction_endpoint}"
    direction_response = requests.post(url=url,
                                       json={
                                  "currency_pair": currency_pair
                              })
    if direction_response.status_code == 200:
        direction = direction_response.json().get("direction")
        logger.info(f"direction response is {direction} for {currency_pair}")
    else:
        logger.error(f"direction response is {direction_response.status_code}")
        raise Exception(f"direction response is {direction_response.status_code}")
    if direction is None:
        return jsonify({"direction":direction,
                        "status": 200})
    #risk
    risk_endpoints = trader_app.config.get("risk_manager").get("endpoints")
    risk_host = trader_app.config.get("risk_manager").get("host")
    risk_port = trader_app.config.get("risk_manager").get("port")
    risk_direction = trader_app.config.get("directions").get(direction)
    ##margin
    open_positions = payload.get("open_positions")
    account_liquidity = payload.get("account_liquidity")
    available_margin = payload.get("available_margin")
    margin_endpoint = risk_endpoints.get("margin_allocator").get("endpoint")
    margin_url = f"http://{risk_host}:{risk_port}{margin_endpoint}"
    margin_response = requests.post(margin_url,
                                    json={
                                     "open_positions": open_positions,
                                     "account_liquidity": account_liquidity,
                                     "available_margin": available_margin
                                  })
    if margin_response.status_code == 200:
        allocated_margin = margin_response.json().get("allocated_margin")
        logger.info(f"allocated margin is {allocated_margin} for {currency_pair}")
    else:
        logger.error(f"risk response is {margin_response.status_code}")
        raise Exception(f"risk response is {margin_response.status_code}")

    ##levels
    current_price = payload.get("current_price")
    levels_endpoint = risk_endpoints.get("levels").get("endpoint")
    levels_url = f"http://{risk_host}:{risk_port}{levels_endpoint}"
    levels_response = requests.post(levels_url,
                                    json={
                                         "current_price": current_price,
                                         "trade_direction": risk_direction,
                                        }
                                    )
    if levels_response.status_code == 200:
        take_profit = levels_response.json().get("take_profit")
        stop_loss = levels_response.json().get("stop_loss")
        logger.info(f"take profit is {take_profit} and stop loss is {stop_loss} for {currency_pair}")
    else:
        logger.error(f"levels response is {levels_response.status_code}")
        raise Exception(f"levels response is {levels_response.status_code}")


    return jsonify(
        identifier=request_identifier,
        direction=direction,
        allocated_margin=allocated_margin,
        take_profit=take_profit,
        stop_loss=stop_loss
    )