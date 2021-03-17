import datetime

from django.db import models


# Create your models here.

class Users(models.Model):
    """
    Users model class

    Attributes:
        username            User's name
        password            User's password
        wallet_number       Unique wallet number, automatically generated (TODO: how to generate)
        total               Total amount of money

    """

    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    wallet_number = models.BigIntegerField(
        default=10000000)  # наличие default значения позволяет вызвать функцию save без конфликтов....
    total = models.IntegerField(default=5000)

    """
    # overrides method in django.model class, found in stackoverflow
    def save(self, *args, **kwargs):
        time_part = int(datetime.datetime.now().timestamp())
        self.wallet_number = int(time_part)
        super(Users, self).save(*args, **kwargs)
    """

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
    sender_wallet_number = models.BigIntegerField()
    receiver_wallet_number = models.BigIntegerField()
    transaction_amount = models.IntegerField()

    def __str__(self):
        return "from {} to {}: {}".format(self.sender_wallet_number, self.receiver_wallet_number,
                                          self.transaction_amount)
