from fastapi.testclient import TestClient

def test_get_all(client: TestClient) -> None:
    response = client.get("/api/airlines")

    assert response.status_code == 200

def test_get_available_codes(client: TestClient) -> None:
    response = client.get("/api/airlines/available-airport-codes")
    codes = response.json()

    assert response.status_code == 200
    assert len(codes) == 29

def test_get_available_years(client: TestClient) -> None:
    response = client.get("/api/airlines/available-years")
    years = response.json()

    assert response.status_code == 200
    assert len(years) == 14

def test_get_available_quantities(client: TestClient) -> None:
    response = client.get("/api/airlines/available-quantities")

    assert response.status_code == 200

def test_get_annual_statistics_404(client: TestClient) -> None:
    response = client.get("/api/airlines/annual-statistics/2000?quantities=num&airport-codes=ord")

    assert response.status_code == 404

def test_get_annual_statistics_422(client: TestClient) -> None:
    response = client.get("/api/airlines/annual-statistics/12?quantities=num&airport-codes=ab")

    assert response.status_code == 422

def test_get_annual_statistics_flights_cancelled(client: TestClient) -> None:
    response = client.get("/api/airlines/annual-statistics/2008?quantities=pct-cancelled&airport-codes=ORD")
    assert response.status_code == 200

    result_json = response.json()

    airport_stats_json = result_json["annual-statistics"]

    actual_elements = len(airport_stats_json)
    assert(actual_elements == 1)

    actual_airport = airport_stats_json[0]["ORD"]

    cancelled_data = actual_airport["pct-cancelled"]

    monthly_data = cancelled_data["monthly_data"]
    expected_data = [8.2, 12.4, 5.7, 4.4, 2.5, 4.7, 3, 2.7, 2.3, 0.8, 1.3, 7.4]
    assert[monthly_data == expected_data]

    

