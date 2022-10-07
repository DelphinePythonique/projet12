from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.
from .models import User


class UserAdmin(BaseUserAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)
        if not "management_team" in request.user.groups.all().values_list(
            "name", flat=True
        ):
            return fieldsets

        if (
            "management_team"
            in request.user.groups.all().values_list("name", flat=True)
            and not request.user.is_superuser
        ):
            fields_to_remove_by_fieldset = {
                _("Personal info"): ("first_name",),
                _("Permissions"): (
                    "user_permissions",
                    "is_superuser",
                ),
            }
            new_fieldsets_dict = {}
            fieldset_with_change = fields_to_remove_by_fieldset.keys()
            for fieldset_name, fieldset_opts in fieldsets:
                if fieldset_name not in fieldset_with_change:
                    new_fieldsets_dict[fieldset_name] = fieldset_opts

                if fieldset_name in fieldset_with_change:
                    field_to_remove = fields_to_remove_by_fieldset[fieldset_name]
                    filtered_fields = [
                        field
                        for field in fieldset_opts["fields"]
                        if field not in field_to_remove
                    ]

                    new_fieldsets_dict[fieldset_name] = {
                        "fields": tuple(filtered_fields)
                    }
            return tuple([(key, value) for key, value in new_fieldsets_dict.items()])
        return fieldsets


admin.site.register(User, UserAdmin)
