from django.contrib import admin

from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost']
    search_fields = ['name', 'cost']
    list_filter = ['cost']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # list_filter = ['student_count']
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ['name', 'education', 'status', 'start', 'finish']
    list_filter = ['status', 'education', 'start', 'finish']
    search_fields = ['name', 'course']


admin.site.register(ClassRoom)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['role', 'name', 'phone']
    list_filter = ['role', 'name', 'phone']
    search_fields = ['name', 'phone']


admin.site.register(Employee)


class EmpTypeAdmin(admin.ModelAdmin):
    list_display = ['role']
    search_fields = ['role']


admin.site.register(EmpType)


