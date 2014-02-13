from django.conf import settings
from userena import views as userena_views


def signup_view(request):
    return userena_views.signup(
        request,
        success_url=settings.USERENA_SIGNIN_REDIRECT_URL,
    )
