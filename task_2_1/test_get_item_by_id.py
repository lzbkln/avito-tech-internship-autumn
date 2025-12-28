import pytest

from util.client import RestItemClient


@pytest.fixture
def client():
    return RestItemClient(base_url="https://qa-internship.avito.com")


def test_get_item_by_id_positive(client):
    item_id = "f44dc749-8edb-48fd-a10d-b8fd679dcc92"
    response = client.get_item_by_id(item_id=item_id)

    # Check response status
    assert response.status_code == 200, "Expected status 200 OK"

    # Check that the response is a list with one element
    assert isinstance(response.json(), list), "Response should be a list"
    assert len(response.json()) == 1, "List should contain one item"

    item = response.json()[0]

    # Check createdAt field
    assert "createdAt" in item, "Missing createdAt field"
    assert len(item["createdAt"].strip()) > 0, "createdAt should not be empty"

    # Check id field
    assert "id" in item, "Missing id field"
    assert isinstance(item["id"], str), "id should be a string"
    assert len(item["id"].strip()) == 36, "id should not be empty"

    # Check name field
    assert "name" in item, "Missing name field"
    assert isinstance(item["name"], str), "name should be a string"
    assert len(item["name"].strip()) > 0, "name should not be empty"

    # Check price field
    assert "price" in item, "Missing price field"
    assert isinstance(item["price"], int), "price should be an integer"

    # Check sellerId field
    assert "sellerId" in item, "Missing sellerId field"
    assert isinstance(item["sellerId"], int), "sellerId should be an integer"

    # Check statistics field
    assert "statistics" in item, "Missing statistics field"
    assert isinstance(item["statistics"], dict), "statistics should be a dictionary"

    # Check statistics.contacts field
    assert "contacts" in item["statistics"], "Missing statistics.contacts field"
    assert isinstance(item["statistics"]["contacts"], int), "statistics.contacts should be an integer"

    # Check statistics.likes field
    assert "likes" in item["statistics"], "Missing statistics.likes field"
    assert isinstance(item["statistics"]["likes"], int), "statistics.likes should be an integer"

    # Check statistics.viewCount field
    assert "viewCount" in item["statistics"], "Missing statistics.viewCount field"
    assert isinstance(item["statistics"]["viewCount"], int), "statistics.viewCount should be an integer"


# Негативные тесты
@pytest.mark.parametrize(
    "item_id, expected_status, expected_message",
    [
        # Некорректный формат ID
        (
                "123",
                400,
                "ID айтема не UUID: 123"
        ),
        # ID не существует
        (
                "8d1424a1-f96f-4fec-8311-c0abc7dd1111",
                404,
                "item 8d1424a1-f96f-4fec-8311-c0abc7dd1111 not found"
        ),
        # Пустой ID
        (
                " ",
                400,
                "ID айтема не UUID:  "
        )
    ],
    ids=[
        "Incorrect ID format",
        "ID does not exist",
        "Empty ID"
    ]
)
def test_get_item_by_id_negative(client, item_id, expected_status, expected_message):
    response = client.get_item_by_id(item_id=item_id)

    assert response.status_code == expected_status
    assert response.json()["result"]["message"] == expected_message
