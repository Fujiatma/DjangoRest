from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
import json

# Create your tests here.


class GetProductsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_products_with_filters(self):
        url = reverse('get_products')
        query_params = {
            'created_from': '2023-06-01',
            'created_to': '2023-08-01',
            'limit': 2
        }
        response = self.client.get(url, query_params)
        self.assertEqual(response.status_code, 200)

    def test_get_products_without_filters(self):
        url = reverse('get_products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



class CreateProductTestCase(TestCase):
    def test_create_product(self):
        url = reverse('create_product')
        payload = [
            {
                "name": "Iphone 11",
                "description": "Iphone 11 new series",
                "variants": [
                    {
                        "name": "IP 11213",
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
                    }
                ]
            }
        ]

        response = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertIn('success create', response_data['message'])
