import pytest

def test_levels_calculator_success(client):
    response = client.post('/risk/levels/', data={
        'current_price': 1.2345,
        'trade_direction': 'buy',
        'take_profit_pips': 20,
        'stop_loss_pips': 10
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'take_profit' in data
    assert 'stop_loss' in data
    assert data['take_profit'] > 1.2345
    assert data['stop_loss'] < 1.2345


def test_levels_calculator_missing_optional(client):
    response = client.post('/risk/levels/', data={
        'current_price': 1.2345,
        'trade_direction': 'short'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert 'take_profit' in data
    assert 'stop_loss' in data
    assert data['take_profit'] < 1.2345
    assert data['stop_loss'] > 1.2345


def test_levels_calculator_invalid_direction(client):
    response = client.post('/risk/levels/', data={
        'current_price': 1.2345,
        'trade_direction': 'booy',
        'take_profit_pips': 15,
        'stop_loss_pips': 5
    })

    assert response.status_code == 400


def test_levels_calculator_missing_required(client):
    response = client.post('/risk/levels/', data={
        'take_profit_pips': 15,
        'stop_loss_pips': 5
    })

    assert response.status_code == 400


