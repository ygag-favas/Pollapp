from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    image = models.ImageField(verbose_name='Image', upload_to="profile_pic/",
                              null=True, blank=True)
    dob = models.DateTimeField(verbose_name='Date of Birth', null=True,
                               default=None, blank=True)
    nick_name = models.CharField(max_length=100, blank=True, null=True)

    def image_tag(self):
        if not self.image:
            """Returns image formated in the given dimensions"""
            img = settings.STATIC_URL + 'polls/images/user-profile' \
                                             '-default-image.png '
        else:
            img = self.image.url
        return format_html('<img src="{}" width="100px" height="100px" />'
                           .format(img))

    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'users'
