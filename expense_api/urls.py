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
    path("sessions/", views.SessionCreateView.as_view(), name="session-create"),
    path(
        "session/",
        views.SessionRetrieveDestroyView.as_view(),
        name="session-retrieve-destroy",
    ),
]
