from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin,
    Group,
    Permission,
)

class Client(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="никнейм",
        max_length=50,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="",
        max_length=50,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name="",
        max_length=50,
        blank=True,
    )
    birthday = models.DateField(
        verbose_name="дата рождения",
        blank=True,
        null=True,  # Fixed
    )
    email = models.EmailField(
        verbose_name="эл. почта",
        max_length=100,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(
        verbose_name="активный",
        default=True,
    )
    is_staff = models.BooleanField(
        verbose_name="сотрудник",
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name="администратор",
        default=False,
    )
    gender = models.CharField(
        verbose_name="пол",
        max_length=10, 
        blank=True,
    )
    date_created = models.DateTimeField(
        verbose_name="дата создания",
        default=timezone.now,
    )
    
    groups = models.ManyToManyField(
        Group, 
        related_name="client_groups",  
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission, 
        related_name="client_permissions", 
        blank=True,
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
