from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, views
from rest_framework.response import Response

from .models import Users, Transaction
from .serializer import SystemUsersSerializer, TransactionSerializer


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = SystemUsersSerializer
    queryset = Users.objects.all()


class TransactionsViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class UsersView(views.APIView):

    def get(self, request):
        messages = Users.objects.all()
        serializer = SystemUsersSerializer(messages)
        return Response(serializer.data)

    def post(self, request):
        serializer = SystemUsersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            message_saved = serializer.save()
        return Response({'Success': "Message {}: {}".format(message_saved.username, message_saved.wallet_number)})


class TransactionsView(views.APIView):

    def get(self, request):
        messages = Transaction.objects.all()
        serializer = TransactionSerializer(messages)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            message_saved = serializer.save()
        return Response({'Success': "Transaction from {} to {} : {}".format(message_saved.sender_wallet_num,
                                                                            message_saved.receiver_wallet_num,
                                                                            message_saved.transaction_amount)})
