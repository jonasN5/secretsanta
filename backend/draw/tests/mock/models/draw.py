from draw.models import Draw
from draw.tests.mock.models.user import userA

draw1_userA = Draw(
    owner=userA,
)
models = [draw1_userA]
