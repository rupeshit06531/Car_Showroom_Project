from django.db import models
from django.utils import timezone


class Car(models.Model):
    car_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    fuel_type = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    


    def __str__(self):
        return self.car_name
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    aadhaar = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    



class Sale(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    employee = models.ForeignKey("Employee", on_delete=models.CASCADE, null=True, blank=True)


    sale_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    sale_date = models.DateField(default=timezone.now)

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        # Auto Invoice Number
        if not self.invoice_number:
            last_sale = Sale.objects.order_by("-id").first()

            if last_sale:
                last_id = last_sale.id + 1
            else:
                last_id = 1

            self.invoice_number = f"INV-{last_id:04d}"

        # Auto Sale Price
        if not self.sale_price:
            self.sale_price = self.car.price

        if self.pk is None:
            if self.car.stock > 0:
              self.car.stock -= 1
              self.car.save()
            else:
                 raise ValueError("Car is Out of Stock")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.name} - {self.car.car_name}"

class Employee(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    joining_date = models.DateField(default=timezone.now)
    photo = models.ImageField(upload_to="employees/", blank=True, null=True)

    def __str__(self):
        return self.name
    
class Supplier(models.Model):

    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class Purchase(models.Model):

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )

    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    purchase_date = models.DateField(
        default=timezone.now
    )

    def save(self, *args, **kwargs):

        # Increase Stock only when creating a new purchase
        if self.pk is None:
            self.car.stock += self.quantity
            self.car.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.car.car_name} ({self.quantity})"