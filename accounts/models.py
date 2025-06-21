from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ON_LEAVE', 'On Leave'),
    ]

    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('STAFF', 'Staff'),
        ('PATIENT', 'Patient'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    phone_number = models.CharField(max_length=20, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')  # <-- new
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
