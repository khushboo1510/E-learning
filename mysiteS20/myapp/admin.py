import decimal

from django.contrib import admin
from .models import Topic, Course, Student, Order
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Topic)
admin.site.register(Order)


def add_50_to_hours(modeladmin, request, queryset):
    for obj in queryset:
        obj.hours = obj.hours + decimal.Decimal('10.0')
        obj.save()


add_50_to_hours.short_description = "Add 10 hours to selected Courses"


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "topic", "price", "hours", "for_everyone"]
    actions = [add_50_to_hours]

    class Meta:
        model = Course


admin.site.register(Course, CourseAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "upper_case_name", "city"]

    def upper_case_name(self, obj):
        return (obj.first_name + " " + obj.last_name).upper()
    upper_case_name.short_description = "Student Full Name"


admin.site.register(Student, StudentAdmin)

