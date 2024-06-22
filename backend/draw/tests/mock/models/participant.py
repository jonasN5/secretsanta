from draw.models import Participant
from draw.tests.mock.models.user import userA

participant0_userA = Participant(
    id=1,
    username=userA.username,
    email=userA.email,
    owner=userA,
)

participant1_userA = Participant(
    id=2,
    username='participant1',
    email='participant1@email.com',
    owner=userA,
)

participant2_userA = Participant(
    id=3,
    username='participant2',
    email='participant2@email.com',
    owner=userA,
)

models = [participant0_userA, participant1_userA, participant2_userA]
