from django.db import models

# Create your models here.


#menu items
class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.IntegerField()
    image=models.URLField()

    def __str__(self):
        return self.name
    
#cart item
class CartItem(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def total_price(self):
        return self.product.price*self.quantity

class Order(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    created_At = models.DateTimeField(auto_now_add=True)
    total = models.IntegerField()

    payment_status = models.CharField(
        max_length=20,
        default="Pending"
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def total_price(self):
        return self.product.price * self.quantity
