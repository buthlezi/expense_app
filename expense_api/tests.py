import jwt
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .factories import ExpenseFactory, UserFactory
from .models import Expense

# from rest_framework_api_key.models import APIKey


# Create your tests here.
class ExpenseTest(TestCase):
    def setUp(self):
        self.client = APIClient()  # self.client is an instance variable
        # api_key, key = APIKey.objects.create_key(name="expense-service")
        # # object, key = APIKey.obj....")
        # self.client.credentials(HTTP_AUTHORIZATION=f"Api-Key {key}")

    def test_create_expense(self):
        url = reverse("expense_api:expense-list-create")
        payload = {
            "amount": 60.0,
            "merchant": "Amazon",
            "description": "Django Rest Framework Book",
        }

        res = self.client.post(url, payload, format="json")
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
        res = self.client.get(url, format="json")
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

        res = self.client.get(
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

        res = self.client.delete(
            url, format="json"
        )  # delete record with id supplied in line 75

        self.assertEqual(status.HTTP_204_NO_CONTENT, res.status_code)
        # assert that record disappears after deletion
        self.assertFalse(Expense.objects.filter(id=expense.id))
        # assert that record cannot be found after deletion

    def test_update_expense(self):
        expense = ExpenseFactory()

        url = reverse("expense_api:expense-retrieve-update-destroy", args=[expense.id])
        payload = {
            "amount": 60.0,
            "merchant": "Amazon",
            "description": "Django Rest Framework Book",
        }
        # replace record created in line 88 with above payload
        res = self.client.put(url, payload, fomat="json")

        updated_expense = Expense.objects.get(id=expense.id)

        # breakpoint()  # explores values generated by class ExpenseFactory in factories.py

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(updated_expense.amount, payload["amount"])
        self.assertEqual(updated_expense.merchant, payload["merchant"])
        self.assertEqual(updated_expense.description, payload["description"])

        # note - tests will certainly fail before the put function is created in views.py

    def test_unsuccessful_expense_update(self):
        expense = ExpenseFactory()

        url = reverse("expense_api:expense-retrieve-update-destroy", args=[expense.id])
        payload = {
            # "amount": 60.0,
            # "merchant": "Amazon",
            "description": "Django Rest Framework Book",
        }

        res = self.client.put(url, payload, fomat="json")
        json_resp = res.json()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, res.status_code)
        self.assertEqual(json_resp["amount"], ["This field is required."])
        self.assertEqual(json_resp["merchant"], ["This field is required."])


class RegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("expense_api:registration-create")

    def test_registration(self):

        payload = {
            "first_name": "Zizi",
            "last_name": "Khumalo",
            "email": "zizi@mail.com",
            "password": "pass123",
            "username": "zizi123",
        }
        # use client to perform post to url using given payload
        res = self.client.post(self.url, payload, format="json")

        json_resp = res.json()
        # using status code to check that record is created
        self.assertEqual(status.HTTP_201_CREATED, res.status_code)
        # checking equality of payload and response values
        self.assertEqual(json_resp["first_name"], payload["first_name"])
        self.assertEqual(json_resp["last_name"], payload["last_name"])
        self.assertEqual(json_resp["email"], payload["email"])
        self.assertEqual(json_resp["username"], payload["username"])

        # check that password not sent back with response
        # a key / password error should be raised if attempt
        # to return password to user is made
        with self.assertRaises(KeyError):
            json_resp["password"]


class SessionCreateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("expense_api:session-create")
        self.user = UserFactory(password="password123")
        # can use UserFactory() but safer to use above just in case
        # default password is changed in UserFactor in factories.py

    def test_create_session(self):
        # we have to use a non-hashed version of password
        payload = {"username": self.user.username, "password": "password123"}
        # note - we haven't used self.user.password bcuz password is hashed

        res = self.client.post(self.url, payload, format="json")

        decoded_token = jwt.decode(
            res.data["jwt"], settings.SECRET_KEY, algorithms=["HS256"]
        )

        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertTrue("jwt" in res.data)
        self.assertEqual(self.user.id, decoded_token["user_id"])


class SessionRetrieveDestroyTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory(password="password123")

    def test_retrieve_session(self):
        # using a non-hashed version of password
        payload = {"username": self.user.username, "password": "password123"}
        # create session
        self.client.post(reverse("expense_api:session-create"), payload, format="json")
        # self...post.reverse('app:endpoint)....'json')

        # retrieve session
        res = self.client.get(
            reverse("expense_api:session-retrieve-destroy"), format="json"
        )

        # check records against user in setUp(self)
        self.assertEqual(status.HTTP_200_OK, res.status_code)
        self.assertEqual(res.data["data"]["id"], self.user.id)
        self.assertEqual(res.data["data"]["first_name"], self.user.first_name)
        self.assertEqual(res.data["data"]["last_name"], self.user.last_name)
        self.assertEqual(res.data["data"]["email"], self.user.email)

    def test_delete_session(self):
        # have to use a non-hashed version of password
        payload = {"username": self.user.username, "password": "password123"}
        # create session
        self.client.post(reverse("expense_api:session-create"), payload, format="json")
        # delete session
        self.client.delete(
            reverse("expense_api:session-retrieve-destroy"), format="json"
        )
        # attempt to retrieve session - this should fail 403 != 200 -
        # until delete fxn is created in views.py
        res = self.client.get(
            reverse("expense_api:session-retrieve-destroy"), format="json"
        )

        self.assertEqual(status.HTTP_403_FORBIDDEN, res.status_code)
