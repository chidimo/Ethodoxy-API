"""Models"""

import uuid

from django.db import models
from django.urls import reverse
from django.conf import settings
# from django.contrib.auth.models import Group
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from sorl.thumbnail import ImageField
from universal.models import TimeStampedModel
from universal.fields import AutoSlugField
from .utils import save_avatar, badge_icon

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("You must provide an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    is_active = models.BooleanField(default=False) # activate by email
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return "User - {}".format(self.email)

    def has_module_perms(self, app_label):
        return True

    def has_perms(self, perm_list, obj=None):
        # print("self", self)
        # print("permissions set", perm_list)
        # print(obj, "object")
        # print(perm_list, 'perm ist')
        # print(obj.creator)
        return True

    def has_perm(self, perm, obj=None):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def siteuser(self):
        return self.siteuser

class SiteUser(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = AutoSlugField(set_using="screen_name")
    screen_name = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    avatar = ImageField(upload_to=save_avatar, null=True, blank=True)

    quota = models.IntegerField(default=1000)
    used = models.IntegerField(default=0)
    key = models.CharField(max_length=50, default=uuid.uuid4, null=True, blank=True, unique=True)

    class Meta:
        ordering = ('created', 'screen_name', )
        verbose_name_plural = 'siteusers'

    @property
    def remaining_quota(self):
        return self.quota - self.used

    def __str__(self):
        return self.screen_name

    def get_absolute_url(self):
        return reverse('siteuser:library', kwargs={'pk' : self.pk, 'slug' : self.slug})

    def get_absolute_uri(self):
        return reverse('douay-rheims:bible_index')

    def get_user_success_url(self):
        pass
        # return reverse()

    def get_user_creation_url(self):
        return reverse('siteuser:new_activation', args=[str(self.user.id), str(self.screen_name)])

class SiteUserPermission(TimeStampedModel):
    name = models.CharField(max_length=50)
    code_name = models.CharField(max_length=50)
    siteuser = models.ManyToManyField(SiteUser)

    class Meta:
        ordering = ("name", )

    def __str__(self):
        return self.name

    @property
    def permitted_siteusers(self):
        return ", ".join([siteuser.screen_name for siteuser in self.siteuser.all()])

class Pontiff(TimeStampedModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    papal_name = models.CharField(max_length=50)
    begin = models.DateField()
    finish = models.DateField()

    def __str__(self):
        return self.papal_name
