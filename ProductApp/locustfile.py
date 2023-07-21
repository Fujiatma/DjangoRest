from locust import HttpUser, task, between
import uuid
import json

class LoadTestProductAPI(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_products(self):
        created_from = "2023-06-01"
        created_to = "2023-08-01"
        limit = 2
        url = f"/v1/products?created_from={created_from}&created_to={created_to}&limit={limit}"
        self.client.get(url)

    @task
    def create_product(self):
        payload = [
            {
                "name": "Iphone 11",
                "description": "Iphone 11 new series",
                "variants": [
                    {
                        "name": "IP 11",
                        "height": 7.5,
                        "stock": 10,
                        "price": 15000000,
                        "weight": 500
                    },
                    {
                        "name": "IP 11 Pro",
                        "height": 8.5,
                        "stock": 5,
                        "price": 20000000,
                        "weight": 700
                    },
                    {
                        "name": "IP 11 Pro Max",
                        "height": 8.5,
                        "stock": 50,
                        "price": 25000000,
                        "weight": 700
                    }
                ]
            },
            {
                "name": "Iphone 12",
                "description": "Iphone 12 new series",
                "variants": [
                    {
                        "name": "IP 12",
                        "height": 7.5,
                        "stock": 20,
                        "price": 17000000,
                        "weight": 500
                    },
                    {
                        "name": "IP 12 Pro",
                        "height": 8.5,
                        "stock": 25,
                        "price": 25000000,
                        "weight": 700
                    }
                ]
            }
        ]
        headers = {'Content-Type': 'application/json'}
        self.client.post("/v1/products/create/", data=json.dumps(payload), headers=headers)