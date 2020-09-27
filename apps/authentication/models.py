import jwt
from django.utils.timezone import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
# from app.apis.models import BaseModel
class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User` for free.
    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """
    def create_user(self, *args, **kwargs):
        """Create and return a `User` with an email, username and password."""
        password = kwargs.get('password', '')
        email = kwargs.get('email', '')
        del kwargs['email']
        del kwargs['password']
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, *args, **kwargs):
        """
        Create and return a `User` with superuser powers.
        Superuser powers means that this use is an admin that can do anything
        they want.
        """
        password = kwargs.get('password', '')
        email = kwargs.get('email', '')
        del kwargs['email']
        del kwargs['password']
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.    

    # user_name = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()
    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return self.email
    @property
    def token(self):
        """
        This method generates and returns a string of the token generated.
        """
        date = datetime.now() + timedelta(hours=24)
        payload = {
            'email': self.email,
            'exp': int(date.strftime('%s')),
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode()
