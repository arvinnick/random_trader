import pytest
from risk_manager.risk_manager_app import risk_app


@pytest.fixture()
def fix_app():
    risk_app.config['TESTING'] = True
    #setup
    risk_app.fixture_level = 1.2345
    risk_app.config.update({
        "reservedMarginPercentage": 0.2,
        "maxVolumePerTrade": 400,
        "numberOfIntendedOpenPositions": 5
    })
    yield risk_app
    #teardown


@pytest.fixture()
def client(fix_app):
    return fix_app.test_client()


@pytest.fixture()
def runner(fix_app):
    return fix_app.test_cli_runner()


