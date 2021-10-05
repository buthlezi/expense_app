import random

import factory
from django.contrib.auth.models import User

from . import models

# models and factories are in the same folder


class ExpenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Expense

    amount = round(random.uniform(5.0, 95.5), 2)
    # random  number btwn 5.0 and 95.5 rounded to 2 dp
    merchant = factory.Faker("company")
    description = factory.Faker("paragraph")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User  # new factory will be saved into user test database

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("word")
    email = factory.Faker("email")
    is_active = True
    password = factory.PostGenerationMethodCall("set_password", "password123")
    # PostGenerationMethodCall generates a hashed password to be stored in database
