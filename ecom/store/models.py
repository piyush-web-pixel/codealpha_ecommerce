from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    pname=models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    pdescription=models.CharField(max_length=200,null=False)
    prize=models.IntegerField(null=False)
    available=models.BooleanField(default=False)
    image = models.ImageField(upload_to='media/product_img')
    discount_price = models.FloatField(blank=True, null=True)  # Optional

    # Optional: auto calculate discount percentage
    @property
    def discount_percent(self):
        if self.discount_price and self.prize:
            return int(100 - (self.discount_price / self.prize * 100))
        return 0

    def is_discounted(self):
        return self.discount_price and self.discount_price < self.prize

 

 
class Register(models.Model):
    regid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50,unique=True)            
    password=models.CharField(max_length=15)
    mobile=models.CharField(max_length=15)
    address=models.CharField(max_length=500)
    city=models.CharField(max_length=20)
    gender=models.CharField(max_length=10)
    status=models.IntegerField()
    role=models.CharField(max_length=10)
    info=models.CharField(max_length=50)





 
class Contact(models.Model):
    regid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50,unique=True)            
    mobile=models.CharField(max_length=15)
    address=models.CharField(max_length=500)
    message=models.CharField(max_length=200)
    city=models.CharField(max_length=20)
    gender=models.CharField(max_length=10)
    info=models.CharField(max_length=50)


# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.FloatField()
#     # Add more fields as needed (image, description, etc.)

#     def __str__(self):
#         return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancelled'),
        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.product.pname} ({self.status})"


# class Women(models.Model):
#     pname=models.CharField(max_length=100)
#     slug = models.SlugField(unique=True, blank=True)
#     pdescription=models.CharField(max_length=200,null=False)
#     prize=models.IntegerField(null=False)
#     available=models.BooleanField(default=False)
#     image = models.ImageField(upload_to='media/product_img')

    

# models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=255)
#     amount = models.FloatField()
#     razorpay_order_id = models.CharField(max_length=100)
#     razorpay_payment_id = models.CharField(max_length=100)
#     payment_status = models.CharField(max_length=20, default="Pending")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.product_name} - {self.user.username}"
