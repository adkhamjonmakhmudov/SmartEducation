from django.contrib import admin

# Register your models here.
from .models import StudentPayment,OutputPayment
@admin.register(StudentPayment)
class StudentPaymentAdmin(admin.ModelAdmin):
    list_filter = ['date']
    list_display = ['student','user','cost','date','type']
    list_per_page = 10
@admin.register(OutputPayment)
class OutPaymentAdmin(admin.ModelAdmin):
      list_display = ['date','cost','user']
      list_per_page = 10