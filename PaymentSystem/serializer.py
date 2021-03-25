from rest_framework import serializers

from PaymentSystem.models import Transaction, Users


class SystemUsersSerializer(serializers.ModelSerializer):
    """
    Serializing all the users
    """

    class Meta:
        model = Users
        fields = ('wallet_number', 'username', 'password', 'total')
        read_only_fields = ('wallet_number',)


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializing all the transactions
    """

    class Meta:
        model = Transaction
        fields = ('sender_wallet_number', 'receiver_wallet_number', 'transaction_amount')
