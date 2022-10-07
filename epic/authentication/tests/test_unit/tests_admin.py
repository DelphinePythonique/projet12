from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client

# Create your tests here.


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
    def setUp(self):
        User = get_user_model()
        admin = User.objects.create(
            username="admin", password="admin", is_superuser=True, is_active=True
        )

        manager_user = User.objects.create(
            username="management", password="admin", is_active=True, is_staff=True
        )
        management_team_group = Group.objects.get(name="management_team")
        management_team_group.user_set.add(manager_user)

        sale_user = User.objects.create(
            username="sales", password="admin", is_active=True, is_staff=True
        )
        management_team_group = Group.objects.get(name="sales_team")
        management_team_group.user_set.add(sale_user)

        support_user = User.objects.create(
            username="supports", password="admin", is_active=True, is_staff=True
        )
        management_team_group = Group.objects.get(name="support_team")
        management_team_group.user_set.add(support_user)

    def test_get_fieldsets(self):
        c = Client()
        c.login(username="admin", password="admin")

        response = c.get("/admin/authentication/user/1/change/", follow=True)
        self.assertRedirects(
            response,
            "/admin/login/?next=%2Fadmin%2Fauthentication%2Fuser%2F1%2Fchange%2F",
            302,
            200,
            fetch_redirect_response=True,
        )
        self.assertContains(response.content, 'id')
