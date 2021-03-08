from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BaseUser(AbstractUser):
    MANAGER = 'manager'
    EMPLOYEE = 'employee'
    ROLE_CHOICES = (
        (MANAGER, 'manager'),
        (EMPLOYEE, 'employee'),
    )

    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(null= False, blank= False)
    phone_number = models.CharField(blank=False, null=True, max_length=10)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=False, null=False)