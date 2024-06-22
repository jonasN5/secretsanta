import pytest

from draw.models import User, Participant


@pytest.mark.django_db
class TestCreateUserParticipant:

    def test_should_create_user_participant(self, client):
        new_user = User(
            email='some_random_email@email.com'
        )
        new_user.save()
        user_participant = Participant.objects.filter(owner=new_user, email=new_user.email).first()
        assert user_participant is not None
