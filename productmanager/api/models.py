from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator


class Product(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(1)],
    )
    description = models.TextField()
    price = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[MinValueValidator(0, "Price cannot be negative.")],
    )
