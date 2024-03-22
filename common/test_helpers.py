from django.test import Client as HttpClient
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


def create_user(email, first_name, last_name):
    if User.objects.filter(email=email).exists():
        return User.objects.get(email=email)

    user = User(
        email=email,
        password="pa55word",
        first_name=first_name,
        last_name=last_name,
        is_superuser=True,
        is_staff=True,
    )
    user.save()

    return user


class BaseTest(TestCase):
    http = None
    user = None

    def setUp(self) -> None:
        self.http = HttpClient()

    def login(self):
        self.http = HttpClient()
        self.user = create_user("admin@user.com", "admin", "user")
        self.http.force_login(User.objects.all().first())

    @property
    def bearer_token(self):
        user = User.objects.all().first()

        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
