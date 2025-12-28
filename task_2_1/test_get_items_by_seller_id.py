import pytest

from util.client import RestItemClient


@pytest.fixture
def client():
    return RestItemClient(base_url="https://qa-internship.avito.com")


def test_get_items_by_seller_id_detailed_check(client):
    seller_id = 123462
    response = client.get_items_by_seller_id(seller_id=seller_id)

    # Check response status
    assert response.status_code == 200, "Expected HTTP status 200 OK"

    # Check that the response is a list
    assert isinstance(response.json(), list), "Response should be a list of items"
    assert len(response.json()) > 0, "Response list should not be empty"

    items = response.json()
    for item in items:
        # Check sellerId field
        assert "sellerId" in item, "Item is missing sellerId field"
        assert isinstance(item["sellerId"], int), "sellerId should be an integer"
        assert item["sellerId"] == seller_id, "sellerId does not match requested ID"

        # Check id field
        assert "id" in item, "Item is missing id field"
        assert isinstance(item["id"], str), "id should be a string"
        assert len(item["id"].strip()) == 36, "id should be a valid UUID (36 characters)"

        # Check name field
        assert "name" in item, "Item is missing name field"
        assert isinstance(item["name"], str), "name should be a string"

        # Check price field
        assert "price" in item, "Item is missing price field"
        assert isinstance(item["price"], int), "price should be an integer"

        # Check createdAt field
        assert "createdAt" in item, "Item is missing createdAt field"
        assert isinstance(item["createdAt"], str), "createdAt should be a string"

        # Check statistics field
        assert "statistics" in item, "Item is missing statistics field"
        assert isinstance(item["statistics"], dict), "statistics should be a dictionary"

        # Check statistics.contacts field
        assert "contacts" in item["statistics"], "Statistics is missing contacts field"
        assert isinstance(item["statistics"]["contacts"], int), "contacts should be an integer"

        # Check statistics.likes field
        assert "likes" in item["statistics"], "Statistics is missing likes field"
        assert isinstance(item["statistics"]["likes"], int), "likes should be an integer"

        # Check statistics.viewCount field
        assert "viewCount" in item["statistics"], "Statistics is missing viewCount field"
        assert isinstance(item["statistics"]["viewCount"], int), "viewCount should be an integer"


def test_get_items_by_valid_seller_id_empty_list(client):
    seller_id = 387265
    response = client.get_items_by_seller_id(seller_id=seller_id)

    # Check response status
    assert response.status_code == 200, "Expected HTTP status 200 OK"

    # Check that the response is an empty list
    assert isinstance(response.json(), list), "Response should be a list"
    assert len(response.json()) == 0, "Response should be an empty list for seller with no items"


# Negative tests
@pytest.mark.parametrize(
    "seller_id, expected_status, expected_message",
    [
        # Incorrect sellerID format (not an integer)
        (
                "abc",
                400,
                "передан некорректный идентификатор продавца"
        ),
        # Negative sellerID
        (
                -123456,
                400,
                "поле seller_id должен быть в диапазоне [111111, 999999]"
        ),
        # Big sellerID
        (
                123456789,
                400,
                "поле seller_id должен быть в диапазоне [111111, 999999]"
        ),
        # Граничные значения поля sellerId
        (
                1000000,
                400,
                "поле seller_id должен быть в диапазоне [111111, 999999]"
        ),

        (
                111110,
                400,
                "поле seller_id должен быть в диапазоне [111111, 999999]"
        ),
    ],
    ids=[
        "Incorrect sellerID format (not an integer)",
        "Negative sellerID",
        "Big sellerID",
        "sellerID above the maximum allowed value",
        "sellerID below minimum allowable value"
    ]
)
def test_get_items_by_seller_id_negative(client, seller_id, expected_status, expected_message):
    response = client.get_items_by_seller_id(seller_id=seller_id)

    # Check error response status
    assert response.status_code == expected_status, "Expected HTTP status 400"

    # Check error response message
    assert "result" in response.json(), "Error response should contain result field"
    assert "message" in response.json()["result"], "Error result should contain message field"
    assert response.json()["result"]["message"] == expected_message, "Error message does not match expected"
