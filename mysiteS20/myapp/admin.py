
from django.contrib import admin
from .models import Topic, Course, Student, Order
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(Topic, Course, Student, Order)
class PersonAdmin(ImportExportModelAdmin):
    pass
