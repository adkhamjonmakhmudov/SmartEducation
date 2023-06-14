from datetime import datetime

from django.db import models, transaction
from django.db.models import ManyToManyField

from center.models import User


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="User", help_text="Select User",
                             null=True, blank=True)
    name = models.CharField(max_length=40, verbose_name="Student Name", help_text="Enter Student Name", null=True,
                            blank=True)
    phone = models.CharField(max_length=15, unique=True, verbose_name="Student Phone Number",
                             help_text="Enter Student Phone Number", null=True, blank=True)
    added = models.DateTimeField(default=datetime.now())
    active = models.BooleanField(default=True)

    one_id = models.PositiveIntegerField(verbose_name="One ID", default=1000, unique=True)
    add_to_course = ManyToManyField('courses.Course', related_name='add_to_course')
    add_to_group = ManyToManyField('courses.Groups', related_name='add_to_group')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.id:
                last_student = Student.objects.order_by('-one_id').first()
                if last_student:
                    self.one_id = last_student.one_id + 1
                super().save(*args, **kwargs)  # Save the student first
            else:
                super().save(*args, **kwargs)

            self.refresh_from_db()
            self.add_to_course.set(self.add_to_course.all())
            self.add_to_group.set(self.add_to_group.all())

    def __str__(self):
        return f"{self.name} | {self.phone} |"

    @property
    def tolov(self):
        data = self.payment.last()
        if data:
            time = data.date
            date_time = time.strftime("%m/%d/%Y, %H:%M:%S")
            return date_time

    class Meta:
        db_table = 'Students'
        verbose_name_plural = "Students"
        ordering = ['-id']


# Davomat Table
class Davomat(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='davomat', to_field='phone')
    status = models.BooleanField(default=True)
    date = models.DateTimeField(default=datetime.now())
    description = models.TextField(default="Sabab ko'rsatilmagan")

    def __str__(self):
        return self.student.name

    class Meta:
        verbose_name = " Attendance "
        verbose_name_plural = " Attendances "

    @property
    def info(self):
        if self.status:
            return '✅'
        else:
            return '❌'
