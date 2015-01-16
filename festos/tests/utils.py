from accounts.models import Profile
from django.contrib.auth.models import User

from documents.models import Document


# Accounts
def create_user(username):
    user = User.objects.create(
        username=username,
        email='{}@email.com'.format(username),
    )
    user.set_password(username)
    user.save()
    return user


def create_profile(username):
    user = get_user(username)
    return Profile.objects.create(user=user)


def get_user(username):
    return User.objects.get(username=username)


def get_profile(username):
    return Profile.objects.get(user__username=username)


def exists_user(username):
    return User.objects.filter(username=username).exists()


def exists_profile(username):
    return Profile.objects.filter(user__username=username).exists()


# Documents
def create_document(title, username):
    if exists_user(username):
        user = get_user(username)
    else:
        user = create_user(username)
    return Document.objects.create(
        title=title,
        owner=user,
        public=False,
    )


def get_document(title):
    return Document.objects.get(title=title)


def exists_document(title):
    return Document.objects.filter(title=title).exists()
