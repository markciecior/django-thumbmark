from django.contrib.auth import get_user_model
from django.test import Client, TestCase

UserModel = get_user_model()


class DjTmScriptViewTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_get_is_not_allowed(self):
        response = self.client.get("/tm/", {"tmid": "attacker-controlled-id"})

        self.assertEqual(response.status_code, 405)
        self.assertFalse(
            UserModel.objects.filter(username="attacker-controlled-id").exists()
        )

    def test_post_without_csrf_token_is_rejected(self):
        response = self.client.post("/tm/", {"tmid": "no-csrf-user"})

        self.assertEqual(response.status_code, 403)
        self.assertFalse(UserModel.objects.filter(username="no-csrf-user").exists())

    def test_post_with_csrf_token_logs_in_and_creates_user(self):
        login_response = self.client.get("/login/?next=/somewhere/")
        csrftoken = login_response.cookies["csrftoken"].value

        response = self.client.post(
            "/tm/",
            {"tmid": "legit-user"},
            HTTP_X_CSRFTOKEN=csrftoken,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"url": "/somewhere/"})
        self.assertTrue(UserModel.objects.filter(username="legit-user").exists())

    def test_authenticated_user_is_not_recreated(self):
        user = UserModel.objects.create_user(username="existing-user")
        login_response = self.client.get("/login/?next=/somewhere/")
        csrftoken = login_response.cookies["csrftoken"].value
        self.client.force_login(user)

        response = self.client.post(
            "/tm/",
            {"tmid": "existing-user"},
            HTTP_X_CSRFTOKEN=csrftoken,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserModel.objects.filter(username="existing-user").count(), 1)


class DjTmLoginViewTests(TestCase):
    def test_login_page_renders_loading_message(self):
        response = self.client.get("/login/?next=/somewhere/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Signing you in", response.content.decode())

    def test_login_page_sets_csrf_cookie(self):
        response = self.client.get("/login/?next=/somewhere/")

        self.assertIn("csrftoken", response.cookies)

    def test_next_is_stashed_in_session(self):
        self.client.get("/login/?next=/somewhere/")

        self.assertEqual(self.client.session["next"], "/somewhere/")


class LoginRequiredThumbmarkDecoratorTests(TestCase):
    def test_unauthenticated_request_redirects_to_login_with_next(self):
        response = self.client.get("/protected/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/?next=/protected/")

    def test_authenticated_request_reaches_view(self):
        user = UserModel.objects.create_user(username="someone")
        self.client.force_login(user)

        response = self.client.get("/protected/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "protected content")
