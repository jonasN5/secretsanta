from django.db.models.signals import post_save
from django.dispatch import receiver

from draw.models import Participant, User


@receiver(post_save, sender=User)
def create_user_participant(sender, **kwargs):
    """Whenever a User is created, also create a Participant object since the user will most likely also participate in
    the draws."""
    created: bool = kwargs.pop('created')
    if created:
        user: User = kwargs.pop('instance')
        Participant.objects.create(
            owner=user,
            username=user.username,
            email=user.email,
        )
