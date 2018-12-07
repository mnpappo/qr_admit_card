from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin, ImportMixin, ExportActionModelAdmin
from django.contrib.auth.models import User, Group


# Register your models here.
from .models import StudentInfo


class StudentInfoResource(resources.ModelResource):
    class Meta:
        model = StudentInfo


class StudentInfoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('student_name', 'roll_no', 'qrimage_tag',)
    readonly_fields = ['image_tag']
    list_per_page = 100
    resource_class = StudentInfoResource


admin.site.site_header = 'Smart Student Admit Info Admin'


admin.site.register(StudentInfo, StudentInfoAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)