import pytest
from analyzer.analyze_app import analyze_app


@pytest.fixture()
def fix_app():
    analyze_app.config['TESTING'] = True
    #setup
    yield analyze_app
    #teardown


@pytest.fixture()
def client(fix_app):
    return fix_app.test_client()


@pytest.fixture()
def runner(fix_app):
    return fix_app.test_cli_runner()