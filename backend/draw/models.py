from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models

from common.models import Timestampable


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, null=True, blank=True, unique=False)
    email = models.EmailField(db_index=True, unique=True, null=False, blank=False)
    password = models.CharField(max_length=256, blank=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()
    objects_unfiltered = models.Manager()

    @property
    def is_staff(self):
        # The admin site requires the is_staff property.
        return self.is_superuser


class Participant(models.Model):
    # The 'admin' for the participant.
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    # The blacklisted participants for this one. We don't assume that blacklisting is symmetrical.
    blacklisted = models.ManyToManyField('self', symmetrical=False)

    class Meta:
        unique_together = ('owner', 'email')


class Draw(Timestampable):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class DrawPair(models.Model):
    santa = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='santa_pairs')
    santee = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='santee_pairs')
    draw = models.ForeignKey(Draw, on_delete=models.CASCADE, related_name='pairs')
