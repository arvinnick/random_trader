import pytest
from trader.app import trader_app


@pytest.fixture()
def fix_app():
    trader_app.config['TESTING'] = True
    #setup
    trader_app.fixed_json_payload = {
            "request_identifier": 12345,
            "current_price": 1.2345,
            "currency_pair":"EURUSD",
            "open_positions": [
                {"symbol": "EURUSD", "volume": 400},
                {"symbol": "USDCHF", "volume": 400},
                {"symbol": "GBPUSD", "volume": 400},
                {"symbol": "AUDUSD", "volume": 400}
            ],
            "account_liquidity": 2800,
            "available_margin": 800
        }
    yield trader_app
    #teardown


@pytest.fixture()
def client(fix_app):
    return fix_app.test_client()


@pytest.fixture()
def runner(fix_app):
    return fix_app.test_cli_runner()


