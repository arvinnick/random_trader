import pytest

def test_levels_calculator_success(client):
    response = client.post('/risk/levels/', json={
        'current_price': client.application.fixture_level,
        'trade_direction': 'buy',
        'take_profit_pips': 20,
        'stop_loss_pips': 10
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'take_profit' in data
    assert 'stop_loss' in data
    assert data['take_profit'] > client.application.fixture_level
    assert data['stop_loss'] < client.application.fixture_level


def test_levels_calculator_missing_optional(client):
    response = client.post('/risk/levels/', json={
        'current_price': client.application.fixture_level,
        'trade_direction': 'short'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'take_profit' in data
    assert 'stop_loss' in data
    assert data['take_profit'] < client.application.fixture_level
    assert data['stop_loss'] > client.application.fixture_level


def test_levels_calculator_invalid_direction(client):
    response = client.post('/risk/levels/', json={
        'current_price': client.application.fixture_level,
        'trade_direction': 'booy',
        'take_profit_pips': 15,
        'stop_loss_pips': 5
    })

    assert response.status_code == 400


def test_levels_calculator_missing_required(client):
    response = client.post('/risk/levels/', json={
        'take_profit_pips': 15,
        'stop_loss_pips': 5
    })

    assert response.status_code == 400



########### margin allocator tests ###########
def test_max_hit_allocation(client):
    response = client.post('/risk/margin_allocator/', json={
        "open_positions": [
            {"symbol": "EURUSD", "volume": 300},
            {"symbol": "USDCHF", "volume": 220}
        ],
        "account_liquidity": 3000,
        "available_margin": 3000 - 300 - 220,
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"allocated_margin": 400}


def test_not_enough_margin(client):
    response = client.post('/risk/margin_allocator/', json={
        "open_positions": [
            {"symbol": "EURUSD", "volume": 400},
            {"symbol": "USDCHF", "volume": 400},
            {"symbol": "GBPUSD", "volume": 400},
            {"symbol": "AUDUSD", "volume": 400}
        ],
        "account_liquidity": 2800,
        "available_margin": 800
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"allocated_margin": 240}



