import pytest

def test_levels_calculator_success(client):
    response = client.post('/', json=client.application.fixed_json_payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data




