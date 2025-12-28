import pytest

from util.client import RestItemClient


@pytest.fixture
def client():
    return RestItemClient(base_url="https://qa-internship.avito.com")

def test_get_statistic_by_id_positive(client):
    item_id = "f44dc749-8edb-48fd-a10d-b8fd679dcc92"
    response = client.get_statistics_by_item_id(item_id=item_id)

    # Check response status
    assert response.status_code == 200, "Expected status 200 OK"

    # Check that the response is a list with one element
    assert isinstance(response.json(), list), "Response should be a list"
    assert len(response.json()) == 1, "List should contain one item"

    statistics = response.json()[0]

    # Check likes field
    assert "likes" in statistics, "Missing likes field"
    assert isinstance(statistics["likes"], int), "likes should be an integer"

    # Check viewCount field
    assert "viewCount" in statistics, "Missing viewCount field"
    assert isinstance(statistics["viewCount"], int), "viewCount should be an integer"

    # Check contacts field
    assert "contacts" in statistics, "Missing contacts field"
    assert isinstance(statistics["contacts"], int), "contacts should be an integer"

# Negative tests
@pytest.mark.parametrize(
    "item_id, expected_status, expected_message",
    [
        # Incorrect ID format
        (
            "123",
            400,
            "передан некорректный идентификатор объявления"
        ),
        # ID does not exist
        (
            "8d1424a1-f96f-4fec-8311-c0abc7dd1111",
            404,
            "statistic 8d1424a1-f96f-4fec-8311-c0abc7dd1111 not found"
        ),
        # Empty ID
        (
            " ",
            400,
            "передан некорректный идентификатор объявления"
        )
    ],
    ids=[
        "Incorrect ID format",
        "ID does not exist",
        "Empty ID"
    ]
)
def test_get_statistic_by_id_negative(client, item_id, expected_status, expected_message):
    response = client.get_statistics_by_item_id(item_id=item_id)

    assert response.status_code == expected_status
    assert response.json()["result"]["message"] == expected_message
