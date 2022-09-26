from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.
from .models import User


class UserAdmin(BaseUserAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)
        if "management_team" in request.user.groups.all().values_list(
            "name", flat=True
        ):
            fields_to_remove = {
                _("Personal info"): ("first_name",),
                _("Permissions"): (
                    "user_permissions",
                    "is_superuser",
                ),
            }
            new_fieldsets_dict = {}

            for name, opts in fieldsets:
                if name not in fields_to_remove.keys():
                    new_fieldsets_dict[name] = opts
                else:
                    list_fields = list(opts["fields"])
                    for field_to_remove in fields_to_remove[name]:
                        list_fields.remove(field_to_remove)
                    new_fieldsets_dict[name] = {"fields": tuple(list_fields)}
            fieldsets = tuple(
                [(key, value) for key, value in new_fieldsets_dict.items()]
            )
        return fieldsets


admin.site.register(User, UserAdmin)
