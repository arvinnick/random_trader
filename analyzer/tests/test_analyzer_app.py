


# direction is in 0, 1, -1
def test_not_enough_margin(client):
    response = client.post('/analyzer/direction/',
                           json={
                               "currency_pair": "EURUSD"
                           })
    assert response.status_code == 200
    data = response.get_json()
    assert 'direction' in data
    assert data['direction'] in {0, 1, None}