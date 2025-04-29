import pytest
from risk_manager.app import risk_app


@pytest.fixture()
def fix_app():
    risk_app.config['TESTING'] = True
    #setup
    yield risk_app
    #teardown


@pytest.fixture()
def client(fix_app):
    return fix_app.test_client()


@pytest.fixture()
def runner(fix_app):
    return fix_app.test_cli_runner()