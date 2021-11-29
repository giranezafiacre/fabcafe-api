from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.fields import EmailField
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
import datetime
from django.utils.timezone import now

class UserManager(BaseUserManager):
    def create_user(self, phone, fullname,image=None, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            
            phone=phone,
             fullname=fullname,image=image
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone,fullname, password,trustworthy):
        """
        Creates and saves a staff user with the given phone and password.
        """
        user = self.create_user(
            
            phone=phone,
             fullname=fullname,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone,fullname,password):
        """
        Creates and saves a superuser with the given phone and password.
        """
        user = self.create_user(
            phone=phone,
             fullname=fullname,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone = PhoneNumberField(unique=True)
    fullname = models.CharField(max_length=30, null=False)
    image = models.ImageField(
        upload_to='uploads',default='../static/img/anonymous.jpg')
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    trustworthy = models.BooleanField(default=False)

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'phone'
    # phone & Password are required by default.
    REQUIRED_FIELDS = ['fullname']

    def get_full_name(self):
        # The user is identified by their email address
        return self.phone

    def get_short_name(self):
        # The user is identified by their email address
        return self.phone

    def __str__(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    objects = UserManager()


class Item(models.Model):
    name = models.CharField(unique=True, max_length=30)
    categories = (
        ('coffee', 'coffee'),
        ('softdrinks', 'softdrinks'),
        ('snacks', 'snacks'),
        ('tea', 'tea'),
    )
    description=models.TextField(max_length=400)
    category = models.CharField(max_length=25, choices=categories)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(null=False)
    image = image = models.ImageField(
        upload_to='uploads', default='../static/img/coffee.PNG')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    delivery_time = models.TimeField(blank=True,null=True)
    order_time_date = models.DateTimeField(default=datetime.datetime.today())
    totalPay=models.DecimalField(max_digits=12, decimal_places=2,default=0)
    ordered = models.BooleanField(default=False,null=False,blank=False)
    paid = models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)
    class meta:
        ordering=['-id']
        
    def __str__(self):
        return f'order for {self.user}'


User = settings.AUTH_USER_MODEL


class OrderItem(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    cart=models.ForeignKey(Order,on_delete=models.CASCADE, related_name="ordered_items", 
    related_query_name="fav_data")
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    categories = (
        ('pending', 'pending'),
        ('available', 'available'),
        ('not_available', 'not_available'),
    )
    availability= models.CharField(max_length=25, choices=categories,default='pending')

    def totalPay(self):
        item=Item.objects.get(id=self.item.id)
        return item.price*self.quantity

    def save(self, *args, **kwargs):
        self.price = self.totalPay()
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'order of {self.quantity} {self.item}s for {self.price}RWF'

class Table(models.Model):
    number_of_persons=models.PositiveIntegerField(default=2)
    reserved_by=models.ForeignKey(User,null=True, on_delete=models.CASCADE)
    categories = (
        ('pending', 'pending'),
        ('available', 'available'),
        ('not_available', 'not_available'),
    )
    availability= models.CharField(max_length=25, choices=categories,default='pending')
    requested_on=models.DateField(default=datetime.date.today())
    time_needed=models.DateTimeField()

class Transaction(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=12, decimal_places=2,default=0)
    paid_on=models.DateTimeField(default=datetime.datetime.today())
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    data=models.JSONField()