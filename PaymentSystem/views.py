from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, views, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Users, Transaction
from .serializer import SystemUsersSerializer, TransactionSerializer

import logging

logging.basicConfig(
    # filename='views.log',
    level=logging.DEBUG)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = SystemUsersSerializer
    queryset = Users.objects.all()


class TransactionsViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class UsersView(views.APIView):

    def get(self, request):
        messages = Users.objects.all()
        serializer = SystemUsersSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SystemUsersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            message_saved = serializer.save()
            return Response(data='added {}'.format(message_saved['username']))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionsView(views.APIView):

    def get_object(self, wallet_number):
        try:
            return Users.objects.get(wallet_number=wallet_number)
        except(Users.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST

    def validate_users(self, wallets):
        for w in wallets:
            try:
                Users.objects.get(wallet_number=w)
            except(Users.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def get(self, request):
        messages = Transaction.objects.all()
        serializer = TransactionSerializer(messages)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        transaction_serializer = TransactionSerializer(data=request.data)
        if transaction_serializer.is_valid(raise_exception=True):
            message_saved = transaction_serializer.save()
            return HttpResponse('added from {} to {}'.format(message_saved['sender_wallet_number'],
                                                             message_saved['receiver_wallet_number']))
        logging.debug('transaction added')

        return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
        sender_wallet_num = request.data['sender_wallet_number']
        receiver_wallet_num = request.data['receiver_wallet_number']
        self.validate_users([sender_wallet_num, receiver_wallet_num])

        sender = self.get_object(sender_wallet_num)
        receiver = self.get_object(receiver_wallet_num)

        sender.total = sender.total - request['transaction_amount']
        receiver.total = receiver.total + receiver['transaction_amount']

        sender.save()
        receiver.save()

        serializer = SystemUsersSerializer([sender, receiver])
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""
