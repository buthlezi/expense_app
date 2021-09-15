from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


# Create your tests here.
class ExpenseTest(TestCase):
    def setUp(self):
        self.clent = APIClient()  # self.clent is an instance variable

    def test_create_expense(self):
        url = reverse("expense_api:expense-list-create")
        payload = {
            "amount": 60.0,
            "merchant": "Amazon",
            "description": "Django Rest Framework Book",
        }

        res = self.clent.post(url, payload, format="json")
        json_resp = res.json()
        # saves res as a json object

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        # checks availability of url

        self.assertEqual(payload["amount"], json_resp["amount"])
        self.assertEqual(payload["merchant"], json_resp["merchant"])
        self.assertEqual(payload["description"], json_resp["description"])
        # checks that data coming from database is equal to data sent to database

        self.assertIsInstance(json_resp["id"], int)
        # checks existence of id of type Instance of an integer
