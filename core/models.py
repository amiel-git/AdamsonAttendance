from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self,email,password=None,**extra_kwargs):

        if not email:
            return ValueError('Please enter an email address')

        email = self.normalize_email(email)
        user = self.model(email,**extra_kwargs)
        user.set_password(password)

        user.save(using=self._db)

        return user


    def create_superuser(self,email,password,**extra_kwargs):

        user = self.create_user(email,password,**extra_kwargs)
        user.is_staff = True
        user.is_superuser = True


class User(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(unique=True,null=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    profile_image = models.ImageField()

    objects = UserManager()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]

    def __str__(self):
        return self.email