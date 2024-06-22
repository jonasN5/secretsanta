from rest_framework.authtoken.models import Token

from draw.tests.mock.models.user import userA

token_userA = Token(
    user=userA,
    key=Token.generate_key(),
)

models = [token_userA]
