from django.db import models
from students.models import Student
from center.models import User
from courses.models import Groups
# Student Payment Table
class StudentPayment(models.Model):
    student = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True,blank=True,related_name='payment')
    group = models.ForeignKey(Groups,on_delete=models.SET_NULL,null=True,blank=True)
    payment_type = (
        ('naqd',"Naqd"),
        ('karta','Karta'),
        ("ko'chirma","Ko'chirma")
    )
    cost = models.CharField(max_length=1000,null=True,blank=True)
    type = models.CharField(max_length=55,choices=payment_type,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField()
    description = models.TextField(null=True,blank=True)
    def __str__(self):
        return f"{self.student.name} {self.cost} so'm to'lov qildi!"
class OutputPayment(models.Model):
    payment_type = (
        ('naqd',"Naqd"),
        ('karta','Karta'),
        ("ko'chirma","Ko'chirma")
    )
    cost = models.CharField(max_length=1000,null=True,blank=True)
    type = models.CharField(max_length=55,choices=payment_type,null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField()
    description = models.TextField(null=True,blank=True)
    def __str__(self):
        return f"{self.cost} so'm xarajat qilindi!"


