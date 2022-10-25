from django.contrib.auth.management import create_permissions
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations


LIST_GROUP_WITH_PERMISSIONS = [
    {
        "group": "support_team",
        "permissions_codenames": [
            "view_contract",
        ],
    },
]


def add_or_remove_permissions_for_group(action, apps, group, permissions_codenames):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
    Group_ = apps.get_model("auth", "Group")
    Permission_ = apps.get_model("auth", "Permission")
    try:
        group = Group_.objects.get(name=group)
    except ObjectDoesNotExist:
        return True
    for permission_codename in permissions_codenames:
        try:
            permission = Permission_.objects.get(codename=permission_codename)
            if action == "add" and permission:
                group.permissions.add(permission)
            if action == "remove" and permission:
                group.permissions.remove(permission)
        except ObjectDoesNotExist:
            pass
    return True


def add_or_remove_permissions_for_groups(action, apps, schema_editors):
    for group_with_permissions in LIST_GROUP_WITH_PERMISSIONS:
        add_or_remove_permissions_for_group(
            action,
            apps,
            group_with_permissions["group"],
            group_with_permissions["permissions_codenames"],
        )


def add_permissions_for_groups(apps, schema_editors):
    add_or_remove_permissions_for_groups("add", apps, schema_editors)


def remove_permissions_for_groups(apps, schema_editors):
    add_or_remove_permissions_for_groups("remove", apps, schema_editors)


class Migration(migrations.Migration):

    dependencies = [
        ("crm", "0003_auto_20221014_1614"),
    ]

    operations = [
        migrations.RunPython(add_permissions_for_groups, remove_permissions_for_groups)
    ]