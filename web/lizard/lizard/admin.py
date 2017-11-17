from django.contrib import admin
from lizard.models import Organisation, Manhole


class UserModelAdmin(admin.ModelAdmin):
    pass


class OrganisationAdmin(admin.ModelAdmin):
    pass


class ManholeAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'organisation_id', 'code',
                    'surface_level', 'width', 'length', 'shape',
                    'bottom_level', 'drainage_area')


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Manhole, ManholeAdmin)
