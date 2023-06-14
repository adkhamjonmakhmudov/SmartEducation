# Create your models here.
from django.db.models import *
from multiselectfield import MultiSelectField

from center.models import *
from students.models import Student


class Course(models.Model):
    name = models.CharField(max_length=100, help_text="Enter course name", verbose_name="Course name")
    cost = models.CharField(max_length=600, verbose_name="Cost", help_text="Enter cost", null=True, blank=True)

    @property
    def student_count(self):
        results = self.groups.all()
        summa = 0
        for result in results:
            summa += len(result.student.all())
        return summa

    @property
    def group_count(self):
        results = self.groups.all()
        return len(results)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Courses"
        verbose_name_plural = "Courses"


class Room(models.Model):
    name = models.CharField(max_length=500, verbose_name="Room name")

    @property
    def group_count(self):
        results = self.groups.all()
        return len(results)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Rooms"
        verbose_name = " Room "
        verbose_name_plural = " Rooms "


class EmpType(models.Model):
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.role

    class Meta:
        db_table = "EmpType"
        verbose_name = " EmpTypes "
        verbose_name_plural = " EmpTypes "


class Employee(models.Model):
    role = models.ForeignKey(EmpType, related_name='roles', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True, verbose_name="Teacher Phone Number",
                             help_text="Enter Teacher Phone Number", null=True, blank=True)
    course = ManyToManyField('courses.Course')
    added = models.DateTimeField()

    def __str__(self):
        return f'{self.role} | {self.name} | {self.phone}'

    class Meta:
        db_table = "Employee"
        verbose_name_plural = "Employees"
        ordering = ['-id']


class Groups(models.Model):
    class Education(models.TextChoices):
        ONLINE = 'online', 'Online'
        OFFLINE = 'offline', 'Offline'

    day = (
        # ('Sun','Sun'),
        ('Mon', 'Mon'),
        ('Tue', 'Tue'),
        ('Wed', 'Wed'),
        ('Thu', 'Thu'),
        ('Fri', 'Fri'),
        ('Sat', 'Sat'),
        ('Sun', 'Sun')
    )

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        WAITING = 'waiting', 'Waiting'

    name = models.CharField(max_length=100, verbose_name="Group name")
    course = models.ManyToManyField('courses.Course', related_name='groups')
    education = models.CharField(max_length=10, choices=Education.choices, null=True, blank=True)
    day = MultiSelectField(max_length=100, choices=day, null=True, blank=True)
    room = models.ManyToManyField('courses.Room', related_name='groups_rooms')
    teacher = models.ManyToManyField('courses.Employee', related_name='teacher')
    status = models.CharField(max_length=10, choices=Status.choices, null=True, blank=True)
    start = models.DateField(null=True, blank=True)
    finish = models.DateField(null=True, blank=True)
    start_lesson = models.TimeField(null=True, blank=True)
    finish_lesson = models.TimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='groupuser')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Grouppa"  # noqa
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    student = models.ManyToManyField(Student, related_name='classes')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='classuser')

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Class Room"
        verbose_name_plural = " Classrooms"
