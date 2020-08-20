
from django.contrib import admin
from .models import Topic, Course, Student, Order
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Topic)
admin.site.register(Order)
admin.site.register(Student)


class CourseAdmin(admin.ModelAdmin):
    list_display = ["name", "topic", "price", "hours", "for_everyone"]

    class Meta:
        model = Course


admin.site.register(Course, CourseAdmin)

