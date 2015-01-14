# Python Imports
import datetime

# Django Imports
from django.db import models
from django.contrib.auth.models import User


class UserExtended(models.Model):
    """
    Main user model. Links into the standard Django User model.
    """
    user = models.OneToOneField(User)
    users_following = models.ForeignKey('UserExtended', blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class UserStatus(models.Model):
    """
    Used to store a users status.

    In this simple prototype application time lines are created from all UserStatus objects.
    """
    user = models.ForeignKey('UserExtended', blank=True, null=True)
    status = models.TextField()
    date_created = models.DateField(default=datetime.date.today())
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.status