from django.contrib import admin

from .models import *


class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone']
    list_filter = ['added']
    search_fields = ['name', 'phone']
    list_per_page = 10
    readonly_fields = ['one_id']

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        student = form.instance
        student.add_to_course.set(form.cleaned_data['add_to_course'])
        student.add_to_group.set(form.cleaned_data['add_to_group'])

    def save_model(self, request, obj, form, change):
        obj.add_to_course.set(obj.add_to_course.all())
        obj.add_to_group.set(obj.add_to_group.all())
        print(obj.user.role)
        if obj.user.role == 'MANAGER' or obj.user.role == 'DIRECTOR':
            super().save_model(request, obj, form, change)
        super().save_model(request, obj, form, change)

    def save_form(self, request, form, change):
        instance = form.save(commit=False)
        instance.save()

        form.save_m2m()  # Save many-to-many relationships after saving the instance

        return instance


admin.site.register(Student, StudentAdmin)


@admin.register(Davomat)
class DavomatAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'info']
    list_filter = ['date', 'status']
    list_per_page = 10
    search_fields = ['student', 'description']
    # def save_model(self, request, obj, form, change):
    #     print(obj.user.role)
    #     if obj.user.role == 'MANAGER' or obj.user.role=='DIRECTOR':
    #         super().save_model(request, obj, form, change)
