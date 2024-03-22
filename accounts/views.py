from django.contrib.auth import get_user_model
from rest_framework import exceptions, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User
from accounts.services import get_tokens_for_user
from accounts.tasks import send_activation_link

from .serializers import UserRegisterSerializer, UserSerializer


class UserRegisterApi(APIView):
    """
    View to register new users
    * Requires no authentication.
    * Non logged in users are able to access this view.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        registered_user = serializer.save()
        send_activation_link.delay(UserSerializer(registered_user).data)
        return Response(UserSerializer(registered_user).data)


class UserLoginApi(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        response = Response()
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed("email and password required")
        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")

        token = get_tokens_for_user(user)
        response.data = token
        return response


class UsersMe(APIView):
    """
    View to get currently logged in user in the system.
    * Requires authentication.
    * Only logged in users are able to access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a serialized request.user object
        """
        return Response(
            UserSerializer(get_user_model().objects.get(email=request.user)).data
        )
