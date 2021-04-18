import uuid

from django.db import models


# Create your models here.


class Users(models.Model):
    """
    Users model class

    Attributes:
        username            User's name
        password            User's password
        wallet_number       Unique wallet number, automatically generated
        total               Total amount of money

    """

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    wallet_number = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True)
    total = models.IntegerField(default=5000)

    def __str__(self):
        return "{} [{}] <{}> : {}".format(self.username, self.password, self.wallet_number, self.total)


class Transaction(models.Model):
    """
    Transaction model class

    Attributes:
        sender_wallet_number        Sender's wallet number
        receiver_wallet_number      Receiver's wallet number
        transaction_amount          Amount of money to send

    """

    sender_wallet_number = models.ForeignKey('Users', related_name='senders_wallet', on_delete=models.RESTRICT)
    receiver_wallet_number = models.ForeignKey(to=Users, related_name='receiver_wallet', on_delete=models.RESTRICT)
    transaction_amount = models.IntegerField()

    def __str__(self):
        return "from {} to {}: {}".format(self.sender_wallet_number, self.receiver_wallet_number,
                                          self.transaction_amount)
