import requests
from requests import Response


class RestItemClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_item(self, seller_id, name, price, likes, view_count, contacts) -> Response:
        url = f"{self.base_url}/api/1/item"
        body = {
            "sellerID": seller_id,
            "name": name,
            "price": price,
            "statistics": {
                "likes": likes,
                "viewCount": view_count,
                "contacts": contacts
            }
        }
        response = requests.post(url, json=body)
        return response

    def get_item_by_id(self, item_id):
        url = f"{self.base_url}/api/1/item/{item_id}"
        response = requests.get(url)
        return response

    def get_items_by_seller_id(self, seller_id):
        url = f"{self.base_url}/api/1/{seller_id}/item"
        response = requests.get(url)
        return response

    def get_statistics_by_item_id(self, item_id):
        url = f"{self.base_url}/api/1/statistic/{item_id}"
        response = requests.get(url)
        return response
