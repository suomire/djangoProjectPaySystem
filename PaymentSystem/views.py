from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, views, status
from rest_framework.exceptions import ValidationError
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def put(self, request):
        sender = request.data['sender_wallet_number']
        receiver = request.data['receiver_wallet_number']
        self.validate_users([sender, receiver])

        sender = self.get_object(sender)
        receiver = self.get_object(receiver)

        sender.total = sender.total - request['transaction_amount']
        receiver.total = receiver.total + receiver['transaction_amount']

        sender.save()
        receiver.save()

        serializer = SystemUsersSerializer([sender, receiver])
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
