# Generated by Django 4.1.7 on 2023-06-14 09:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_classroom_options_alter_course_options_and_more'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Students'},
        ),
        migrations.AddField(
            model_name='student',
            name='add_to_course',
            field=models.ManyToManyField(related_name='add_to_course', to='courses.course'),
        ),
        migrations.AddField(
            model_name='student',
            name='add_to_group',
            field=models.ManyToManyField(related_name='add_to_group', to='courses.groups'),
        ),
        migrations.AddField(
            model_name='student',
            name='one_id',
            field=models.PositiveIntegerField(default=1000, unique=True, verbose_name='One ID'),
        ),
        migrations.AlterField(
            model_name='davomat',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 47, 37, 228616)),
        ),
        migrations.AlterField(
            model_name='student',
            name='added',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 14, 14, 47, 37, 227407)),
        ),
    ]