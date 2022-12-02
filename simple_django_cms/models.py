import datetime
import uuid

from django.core.cache import cache
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models
from django.db.models import Q
from django.shortcuts import reverse
from django.utils.text import slugify

from . import constants
from .conf import settings
from . import managers


class User(AbstractUser):

    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = managers.CustomUserManager()

    def save(self, *args, **kwargs):
        creation = getattr(self, 'id', None) is None
        if self.email in [None, '', ' ']:
            raise ValidationError('Email is required')
        self.email = self.email.lower()
        self.username = self.email
        super(User, self).save(*args, **kwargs)


# --

class Project(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_admin_items_url(self):
        return reverse(
            constants.URLNAME_ADMIN_LIST_ITEMS,
            kwargs={
                'project_id': str(self.id)
            }
        )

    def get_admin_url(self):
        return self.get_admin_items_url()

    def __str__(self):
        return self.name


class ProjectAdmin(models.Model):

    class Meta:
        unique_together = ('project', 'user')

    ACL_CHOICES_ADMIN = ('admin', 'Admin')
    ACL_CHOICES = (
        ACL_CHOICES_ADMIN,
    )

    ACL_CHOICE_DEFAULT = str(ACL_CHOICES_ADMIN[0])

    project = models.ForeignKey('Project', related_name='users', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='projects', on_delete=models.CASCADE)
    acl = models.CharField(max_length=255, choices=ACL_CHOICES, default=ACL_CHOICE_DEFAULT)


# --

class Tenant(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('Tenant', related_name='children', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class TenantUser(models.Model):

    class Meta:
        unique_together = ('tenant', 'user')

    ACL_CHOICES_ADMIN = ('admin', 'Admin')
    ACL_CHOICES_USER = ('user', 'User')
    ACL_CHOICES = (
        ACL_CHOICES_ADMIN,
        ACL_CHOICES_USER
    )

    ACL_CHOICE_DEFAULT = str(ACL_CHOICES_USER[0])

    tenant = models.ForeignKey('Tenant', related_name='users', on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='tenants', on_delete=models.CASCADE)
    acl = models.CharField(max_length=255, choices=ACL_CHOICES, default=ACL_CHOICE_DEFAULT)


# --

class Tenancy(models.Model):

    class Meta:
        unique_together = ('project', 'tenant')

    project = models.ForeignKey('Project', related_name='tenants', on_delete=models.CASCADE)
    tenant = models.ForeignKey('Tenant', related_name='projects', on_delete=models.CASCADE)


# --

class Item(models.Model):

    data = models.JSONField(default=dict)
    content_type = models.CharField(max_length=255, db_index=True)
    #
    project = models.ForeignKey('Project', related_name='items', on_delete=models.CASCADE)
    tenant = models.ForeignKey('Tenant', related_name='items', on_delete=models.CASCADE, blank=True, null=True)
    #
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ItemRelation(models.Model):

    child = models.ForeignKey('Item', related_name='parents', on_delete=models.CASCADE)
    parent = models.ForeignKey('Item', related_name='children', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, db_index=True)
