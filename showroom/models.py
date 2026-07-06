from django.db import models


class Car(models.Model):
    car_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.car_name