from django.db import models
from django.contrib.auth.models import User


class Dealer(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    full_name = models.CharField(max_length=200, blank=True)
    st = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    review = models.TextField()
    sentiment = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dealer.name} - {self.user.username}"