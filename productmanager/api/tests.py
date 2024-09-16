import json

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Product


class TestIndex(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)


class TestProducts(TestCase):
    def setUp(self):
        self.product_to_post = {
            "name": "New Product",
            "description": "This is a new product.",
            "price": 29.99,
        }
        self.url = reverse("products")

    def test_get_empty_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_post_valid_product(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.product_to_post),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.json()["name"], self.product_to_post["name"])

    def test_post_invalid_product(self):
        new_product_data = {
            "name": "",
            "description": "",
            "price": -0.121631,
        }
        current_product_count = Product.objects.count()

        response = self.client.post(
            self.url, data=json.dumps(new_product_data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        errors = response.json()["errors"]
        self.assertEquals(errors.get("name"), ["This field cannot be blank."])
        self.assertEquals(
            errors.get("price"),
            [
                "Price cannot be negative.",
                "Ensure that there are no more than 2 decimal places.",
            ],
        )
        self.assertEqual(current_product_count, Product.objects.count())

    def test_get_products(self):
        Product.objects.create(**self.product_to_post)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["name"], self.product_to_post["name"])
        self.assertTrue(isinstance(response.json()[0]["price"], float))
