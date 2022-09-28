from django.conf import settings
from django.test import TestCase

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
        User =  settings.AUTH_USER_MODEL
        admin = User.objects.create(username="admin")

        user = User.objects.create(username="management")

        User.objects.create(username="sales")
        User.objects.create(username="supports")


    def test_get_fieldsets(self):
        pass