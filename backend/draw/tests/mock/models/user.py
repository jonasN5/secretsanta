from draw.models import User

userA = User(
    username='userA',
    email='usera@email.com',
)
userA.set_password('userA_password')  # Passwords must be hashed

userB = User(
    username='userB',
    email='userb@email.com',
)
userB.set_password('userB_password')  # Passwords must be hashed

models = [userA, userB]
