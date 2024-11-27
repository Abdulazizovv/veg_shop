from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    """Define a manager for the CustomUser without the username field."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# for custom user 
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_seller = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=25, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# for profile
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} Profile'


# for product
class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('fruit', 'Fruit'),
        ('vegetable', 'Vegetable'),
    ]
    
    CATEGORY_CHOICES = [
        ('A', 'Category A'),
        ('B', 'Category B'),
        ('C', 'Category C'),
        ('D', 'Category D'),
    ]
    
    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPE_CHOICES)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    # Image fields for each category
    image_A = models.ImageField(upload_to='products/category_A/', blank=True, null=True)
    image_B = models.ImageField(upload_to='products/category_B/', blank=True, null=True)
    image_C = models.ImageField(upload_to='products/category_C/', blank=True, null=True)
    image_D = models.ImageField(upload_to='products/category_D/', blank=True, null=True)

    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Set default images if B, C, or D images are not provided
        if not self.image_B and self.image_A:
            self.image_B = self.image_A
        if not self.image_C and self.image_A:
            self.image_C = self.image_A
        if not self.image_D and self.image_A:
            self.image_D = self.image_A
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.get_product_type_display()}) - {self.get_category_display()}"
    
    def get_category_image(self):
        """Returns the image associated with the product's category."""
        if self.category == 'A':
            return self.image_A
        elif self.category == 'B':
            return self.image_B
        elif self.category == 'C':
            return self.image_C
        elif self.category == 'D':
            return self.image_D
        return None


class BuyerInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    
    def __str__(self):
        return f"{self.user} - {self.phone_number}"


class SoldProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    CATEGORY_CHOICES = [
        ('A', 'Category A'),
        ('B', 'Category B'),
        ('C', 'Category C'),
        ('D', 'Category D'),
    ]
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default="A")
    address = models.TextField()
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status_choices = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    date_sold = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} units sold on {self.date_sold}"



# django signals 

# @receiver(post_save, sender=CustomUser)
# def create_profile(sender, instance, created,**kwargs):
#     if created:
#         Profile.objects.create(user=CustomUser)
