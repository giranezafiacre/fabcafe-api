from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

class UserManager(BaseUserManager):
    def create_user(self, phone, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            phone=phone,
            first_name=first_name, last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, first_name, last_name, password):
        """
        Creates and saves a staff user with the given phone and password.
        """
        user = self.create_user(
            phone,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, first_name, last_name, password):
        """
        Creates and saves a superuser with the given phone and password.
        """
        user = self.create_user(
            phone,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone = PhoneNumberField(unique=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    image = models.ImageField(
        upload_to='uploads', default='../../static/img/anonymous.jpg')
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    trustworthy = models.BooleanField(default=False)

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'phone'
    # phone & Password are required by default.
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.phone

    def get_short_name(self):
        # The user is identified by their email address
        return self.phone

    def __str__(self):
        return str(self.first_name)

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
    name = models.CharField(unique=True,max_length=30)
    categories = (
        ('1', 'coffee'),
        ('2', 'softdrinks'),
        ('3', 'snacks'),
    )
    category = models.CharField(max_length=25, choices=categories, default='1')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = image = models.ImageField(
        upload_to='uploads', default='../../static/img/coffee.PNG')

    def __str__(self):
        return self.name


User = settings.AUTH_USER_MODEL


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    order_time = models.TimeField(auto_now=True)
    delivery_time = models.TimeField(auto_now=False, auto_now_add=False)
    TotalPay= models.DecimalField(max_digits=12, decimal_places=2)
    paid =models.BooleanField(default=False)

    def __str__(self):
        return f'order {self.id} for {self.user}'
