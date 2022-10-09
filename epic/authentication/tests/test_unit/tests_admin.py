from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client


User = get_user_model()


def mocked_super_get_fieldsets():
    return (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


class TestUserAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.superuser= User.objects.create_superuser(
            username="admin", password="admin"
        )

        cls.manager_user = User.objects.create_user(
            username="management", password="admin", is_active=True, is_staff=True
        )
        management_team_group = Group.objects.get(name="management_team")
        management_team_group.user_set.add(cls.manager_user)

        cls.sale_user = User.objects.create_user(
            username="sales", password="admin", is_active=True, is_staff=True
        )
        management_team_group = Group.objects.get(name="sales_team")
        management_team_group.user_set.add(cls.sale_user)

        cls.support_user = User.objects.create_user(
            username="supports", password="admin", is_active=True, is_staff=True
        )
        management_team_group = Group.objects.get(name="support_team")
        management_team_group.user_set.add(cls.support_user)

    def test_get_fieldsets(self):
        client = Client()

        client.force_login(TestUserAdmin.superuser)
        response = client.get("/admin/authentication/user/1/change/")
        self.assertEqual(response.status_code, 200)
        html_response = response.content.decode("utf-8")
        self.assertIn("id_is_superuser", html_response)

        client.force_login(TestUserAdmin.superuser)
        response = client.get("/admin/authentication/user/1/change/")
        self.assertEqual(response.status_code, 200)
        html_response = response.content.decode("utf-8")
        self.assertIn("id_is_superuser", html_response)
