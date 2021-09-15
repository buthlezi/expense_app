from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ExpenseSerializer


# Create your views here.
class ExpensesListCreateView(APIView):
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # implies serializer not valid
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

