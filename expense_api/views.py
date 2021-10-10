# from django.shortcuts import get_object_or_404
# from rest_framework import status
from django.contrib.auth.models import User
from rest_framework import exceptions, status
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from expense_api.authentication import JWTAuthentication, generate_access_token

from .models import Expense
from .serializers import ExpenseSerializer, UserSerializer

# from rest_framework_api_key.permissions import HasAPIKey


# from expense_api.factories import ExpenseFactory


# from rest_framework.response import Response
# from rest_framework.views import APIView


# Create your views here.

# class ExpenseListCreateView(APIView):
# replace with:
class ExpenseListCreateView(ListCreateAPIView):
    # def post(self, request):
    #     serializer = ExpenseSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     # if serializer is not valid
    #     return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # # useful activity - compare post and get functions

    # def get(self, request):
    #     expenses = Expense.objects.all()
    #     # uses Django objects to fetch all expense ecords and assign to expenses variable
    #     serializer = ExpenseSerializer(expenses, many=True)
    #     # multiple expense records passed to serializer variable
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # replace with:
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    # permission_classes = [HasAPIKey]

    # protection added below
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


# class ExpenseRetrieveUpdateDestroyView(APIView):
# replace with:
class ExpenseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    # def get(self, request, pk):  # note the primary key as expected in urls.py line 12
    #     expense = get_object_or_404(Expense, pk=pk)
    #     # look in Expense model and find any record that matches pk in line 31
    #     serializer = ExpenseSerializer(expense, many=False)
    #     # serializes found record
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def delete(self, request, pk):
    #     expense = get_object_or_404(Expense, id=pk)
    #     expense.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def put(self, request, pk):
    #     expense = get_object_or_404(Expense, id=pk)  # fetch record to be updated
    #     serializer = ExpenseSerializer(
    #         expense, data=request.data
    #     )  # pass original data and payload data
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             serializer.data, status=status.HTTP_200_OK
    #         )  # return updated data
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     # otherwise return error
    # replace with:
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    # permission_classes = [HasAPIKey]

    # protection added below
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class RegistrationCreateView(CreateAPIView):
    serializer_class = UserSerializer


class SessionCreateView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = get_object_or_404(User, username=username)

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed(
                "Incorrect Password", code=status.HTTP_401_UNAUTHORIZED
            )

        # # temp token
        # token = "temptokenhere"

        token = generate_access_token(user)

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt": token}

        return response  # returns 'jwt': 'temptokenhere'


class SessionRetrieveDestroyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        # serialize user from get request
        # user authenticated by auth_class and perm_classes
        return Response({"data": serializer.data})
        # data retrieved from serializer

    def delete(self, request):
        response = Response()
        response.delete_cookie(
            key="jwt"
        )  # delete cookie on user's browser that has 'jwt' key
        response.data = {"message": "Logged out"}

        return response
