from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from expense_api.factories import ExpenseFactory

from .models import Expense
from .serializers import ExpenseSerializer


# Create your views here.
class ExpenseListCreateView(APIView):
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if serializer is not valid
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    # useful activity - compare post and get functions

    def get(self, request):
        expenses = Expense.objects.all()
        # uses Django objects to fetch all expense ecords and assign to expenses variable
        serializer = ExpenseSerializer(expenses, many=True)
        # multiple expense records passed to serializer variable
        return Response(serializer.data, status=status.HTTP_200_OK)


class ExpenseRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):  # note the primary key as expected in urls.py line 12
        expense = get_object_or_404(Expense, pk=pk)
        # look in Expense model and find any record that matches pk in line 31
        serializer = ExpenseSerializer(expense, many=False)
        # serializes found record
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        expense = get_object_or_404(Expense, id=pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        expense = get_object_or_404(Expense, id=pk)  # fetch record to be updated
        serializer = ExpenseSerializer(
            expense, data=request.data
        )  # pass original data and payload data
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )  # return updated data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # otherwise return error

