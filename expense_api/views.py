from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Expense
from .serializers import ExpenseSerializer


# Create your views here.
class ExpensesListCreateView(APIView):
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
