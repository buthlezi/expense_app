from django.urls import path

from . import views

# urls.py and views.py are in the same folder 'expense_api'

urlpatterns = [
    path(
        "expenses/", views.ExpensesListCreateView.as_view(), name="expense-list-create"
    )
]
