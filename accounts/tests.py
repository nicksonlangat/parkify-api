from accounts.models import User
from common.test_helpers import BaseTest


# Create your tests here.
class AuthenticationTest(BaseTest):
    def setUp(self) -> None:
        self.login()

    @staticmethod
    def _get_new_user_data():
        return {
            "email": "new_user@email.com",
            "first_name": "new",
            "last_name": "user",
            "phone_number": "0701010101",
            "password": "@pa55word",
        }

    def test_view_me(self):
        response = self.http.get("/accounts/users/me", **self.bearer_token)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "email")

    def test_register_user(self):
        path = "/accounts/register/"
        response = self.http.get(path)
        self.assertEqual(405, response.status_code)

        data = self._get_new_user_data()

        post = self.http.post(path, data)
        user = User.objects.get(email=data["email"])

        self.assertIsNotNone(user)
        self.assertNotIn(response.content.__str__(), "Error")
        self.assertEqual(200, post.status_code)
        self.assertNotIn("None", user.first_name)
