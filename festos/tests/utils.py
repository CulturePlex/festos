from accounts.models import Profile
from django.contrib.auth.models import User


def create_user(username):
    user = User.objects.create(
        username=username,
        email='{}@email.com'.format(username),
    )
    user.set_password(username)
    user.save()
    return user


def create_profile(user):
    return Profile.objects.create(user=user)


def get_user(username):
    return User.objects.get(username=username)


def get_profile(username):
    return Profile.objects.get(user__username=username)


def exists_user(username):
    return User.objects.filter(username=username).exists()


def exists_profile(username):
    return Profile.objects.filter(user__username=username).exists()
