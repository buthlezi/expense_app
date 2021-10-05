from django.urls import path

from . import views

# urls.py and views.py are in the same folder 'expense_api'

urlpatterns = [
    path(
        "expenses/", views.ExpenseListCreateView.as_view(), name="expense-list-create"
    ),
    path(
        "expenses/<str:pk>",  # always has a primary key
        views.ExpenseRetrieveUpdateDestroyView.as_view(),
        name="expense-retrieve-update-destroy",
    ),
    path(
        "registrations/",
        views.RegistrationCreateView.as_view(),
        name="registration-create",
    ),
]
