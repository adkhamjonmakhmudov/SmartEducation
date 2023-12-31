# Generated by Django 4.1.7 on 2023-06-10 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        ('students', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.CharField(blank=True, max_length=1000, null=True)),
                ('type', models.CharField(blank=True, choices=[('naqd', 'Naqd'), ('karta', 'Karta'), ("ko'chirma", "Ko'chirma")], max_length=55, null=True)),
                ('date', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.groups')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment', to='students.student')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OutputPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.CharField(blank=True, max_length=1000, null=True)),
                ('type', models.CharField(blank=True, choices=[('naqd', 'Naqd'), ('karta', 'Karta'), ("ko'chirma", "Ko'chirma")], max_length=55, null=True)),
                ('date', models.DateTimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
