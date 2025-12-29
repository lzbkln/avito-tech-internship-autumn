import pytest

from util.client import RestItemClient


@pytest.fixture
def client():
    return RestItemClient(base_url="https://qa-internship.avito.com")


@pytest.mark.parametrize(
    "seller_id, name, price, statistics, expected_status",
    [
        # Успешное создание объявления
        (
                345123,
                "ipad",
                40000,
                {"contacts": 5, "likes": 2, "viewCount": 50},
                200
        ),
        # Проверка граничных значений поля sellerID
        (
                111111,
                "iphone",
                45000,
                {"contacts": 2, "likes": 2, "viewCount": 50},
                200
        ),
        (
                999999,
                "iphone",
                45000,
                {"contacts": 2, "likes": 2, "viewCount": 50},
                200
        ),
        # Нулевое значение поля contacts
        (
                345123,
                "iPhone",
                40000,
                {"contacts": 0, "likes": 2, "viewCount": 5},
                200
        ),
        # Нулевое значение поля likes
        (
                345123,
                "iPhone",
                40000,
                {"contacts": 2, "likes": 0, "viewCount": 5},
                200
        ),
        # Нулевые значения полей в statistics
        (
                345123,
                "iPhone",
                40000,
                {"contacts": 0, "likes": 0, "viewCount": 0},
                200
        ),
        # Нулевое значение поля price
        (
                345123,
                "iPhone",
                0,
                {"contacts": 2, "likes": 2, "viewCount": 5},
                200
        )
    ],
    ids=[
        "Successful creation of an ad with matching data",
        "Create ad with minimum valid sellerID",
        "Create ad with maximum allowed sellerID",
        "Creating an ad with a zero value contacts",
        "Creating an ad with zero likes",
        "Zero values of fields in statistics",
        "Creating an ad with a value of zero price"
    ]
)
def test_create_item_positive(
        client,
        seller_id,
        name,
        price,
        statistics,
        expected_status
):
    response = client.create_item(
        seller_id=seller_id,
        name=name,
        price=price,
        likes=statistics["likes"],
        view_count=statistics["viewCount"],
        contacts=statistics["contacts"]
    )

    assert response.status_code == expected_status


@pytest.mark.parametrize(
    "seller_id, name, price, statistics, expected_status",
    [
        # Проверка граничных значений поля sellerID
        (
                111110,
                "iPhone",
                40000,
                {"contacts": 1, "likes": 2, "viewCount": 5},
                400
        ),
        (
                1000000,
                "iPhone",
                40000,
                {"contacts": 1, "likes": 2, "viewCount": 5},
                400
        ),
        # Проверка строкового представления поля sellerID
        (
                "abc",
                "iPhone",
                40000,
                {"contacts": 1, "likes": 2, "viewCount": 5},
                400
        ),
        # Негативное значение поля price
        (
                345123,
                "iPhone",
                -40000,
                {"contacts": 1, "likes": 2, "viewCount": 5},
                400
        ),
        # Негативное значение поля contacts
        (
                345123,
                "iPhone",
                40000,
                {"contacts": -10, "likes": 2, "viewCount": 5},
                400
        ),
        # Негативное значение поля likes
        (
                345123,
                "iPhone",
                40000,
                {"contacts": 1, "likes": -35, "viewCount": 5},
                400
        ),
        # Негативное значение поля viewCount
        (
                345123,
                "iPhone",
                40000,
                {"contacts": 1, "likes": 2, "viewCount": -5},
                400
        ),
        # Нулевое значение поля viewCount (т.к поле likes > 0 и contacts > 0, то viewCount > 0) (business logic)
        (
                345123,
                "iPhone",
                40000,
                {"contacts": 10, "likes": 2, "viewCount": 0},
                400
        ),
        # Поле viewCount <= likes (business logic)
        (
                345123,
                "iPhone",
                40000,
                {"contacts": 1, "likes": 100, "viewCount": 5},
                400
        ),
        # Поле viewCount <= contacts (business logic)
        (
                345123,
                "iPhone",
                40000,
                {"contacts": 100, "likes": 2, "viewCount": 5},
                400
        ),
        # Поле name пустое
        (
                345123,
                "",
                40000,
                {"contacts": 1, "likes": 2, "viewCount": 5},
                400
        ),
        # Поле name None
        (
                345123,
                None,
                40000,
                {"contacts": 1, "likes": 2, "viewCount": 5},
                400
        ),
        # Поле price слишком большое
        (
                345123,
                "iPhone",
                4000000000000000000000,
                {"contacts": 1, "likes": 2, "viewCount": 5},
                400
        )
    ],
    ids=[
        "sellerID below minimum allowable value",
        "sellerID above the maximum allowed value",
        "Check string view field sellerID",
        "Negative value price",
        "Negative value contacts",
        "Negative value of likes",
        "Negative viewCount value",
        "Zero viewCount value for non-zero likes and contacts",
        "viewCount less than likes",
        "viewCount is smaller than contacts",
        "Empty value name",
        "name value is None",
        "Too large value price"
    ]
)
def test_create_item_negative(
        client,
        seller_id,
        name,
        price,
        statistics,
        expected_status
):
    response = client.create_item(
        seller_id=seller_id,
        name=name,
        price=price,
        likes=statistics["likes"],
        view_count=statistics["viewCount"],
        contacts=statistics["contacts"]
    )

    assert response.status_code == expected_status
