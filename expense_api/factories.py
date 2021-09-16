import random

import factory

from . import models

# models and factories are in the same folder


class ExpenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Expense

    amount = round(random.uniform(5.0, 95.5), 2)
    # random  number btwn 5.0 and 95.5 rounded to 2 dp
    merchant = factory.Faker("company")
    description = factory.Faker("paragraph")

