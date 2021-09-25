from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .factories import ExpenseFactory
from .models import Expense


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
        # breakpoint()
        json_resp = res.json()
        # saves res as a json object

        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        # equivalent to self.assertEqual(201, res.status_code)
        # checks availability of url

        self.assertEqual(payload["amount"], json_resp["amount"])
        self.assertEqual(payload["merchant"], json_resp["merchant"])
        self.assertEqual(payload["description"], json_resp["description"])
        # checks that data coming from database is equal to data sent to database

        self.assertIsInstance(json_resp["id"], int)
        # checks existence of id of type Instance of an integer

    def test_list_expenses(self):
        expense = ExpenseFactory()
        # creates record in test database by calling Expensefactory from factories.py

        url = reverse("expense_api:expense-list-create")
        # expense-list-create handles creating and listing of records
        res = self.clent.get(url, format="json")
        # extracts a number of records

        json_resp = res.json()
        # breakpoint()

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(expense.amount, json_resp[0]["amount"])
        self.assertEqual(expense.merchant, json_resp[0]["merchant"])
        self.assertEqual(expense.description, json_resp[0]["description"])

    def test_retrieve_expense(self):
        expense = ExpenseFactory()  # create records in test database

        url = reverse("expense_api:expense-retrieve-update-destroy", args=[expense.id])

        res = self.clent.get(
            url, format="json"
        )  # expense.id used to find a particular record
        json_resp = res.json()

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        # check that retrieved record (JSON object) matches the created record
        self.assertEqual(expense.amount, json_resp["amount"])
        self.assertEqual(expense.merchant, json_resp["merchant"])
        self.assertEqual(expense.description, json_resp["description"])

    def test_delete_expense(self):
        expense = ExpenseFactory()

        url = reverse("expense_api:expense-retrieve-update-destroy", args=[expense.id])

        res = self.clent.delete(
            url, format="json"
        )  # delete record with id supplied in line 75

        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)
        # assert that record disappears after deletion
        self.assertFalse(Expense.objects.filter(id=expense.id))
        # assert that record cannot be found after deletion

