from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, views, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Users, Transaction
from .serializer import UsersSerializer, TransactionSerializer

import logging

logging.basicConfig(
    # filename='views.log',
    level=logging.DEBUG)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.all()


class TransactionsViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class UsersView(views.APIView):

    def get(self, request):
        messages = Users.objects.all()
        serializer = UsersSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UsersSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            message_saved = serializer.save()
            return Response({"success": "User added {}".format(message_saved.username)})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionsView(views.APIView):

    def get_object(self, wallet_number):
        """
        Get user instance using unique wallet number

        :param wallet_number:
        :return: User object or raise HTTP_400_BAD_REQUEST
        """
        try:
            return Users.objects.get(wallet_number=wallet_number)
        except(Users.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST

    def validate_users(self, wallets):
        """
        Validate users' wallets that participate in transaction

        :param wallets: list wallet ids of sender and receiver
        :return: True or raise HTTP_400_BAD_REQUEST
        """
        for w in wallets:
            try:
                Users.objects.get(wallet_number=w)
            except(Users.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True

    def get(self, request):
        messages = Transaction.objects.all()
        serializer = TransactionSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        sender_wallet_num = request.data['sender_wallet_number']
        receiver_wallet_num = request.data['receiver_wallet_number']
        self.validate_users([sender_wallet_num, receiver_wallet_num])

        sender = self.get_object(sender_wallet_num)
        receiver = self.get_object(receiver_wallet_num)

        # update users total info
        sender.total = sender.total - request.data['transaction_amount']
        receiver.total = receiver.total + request.data['transaction_amount']

        # save instances
        sender.save()
        receiver.save()

        # add transaction to db
        transaction_serializer = TransactionSerializer(data=request.data)
        if transaction_serializer.is_valid(raise_exception=True):
            transaction_serializer.save()
            return Response(transaction_serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(transaction_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
