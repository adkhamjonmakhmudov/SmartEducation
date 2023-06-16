from rest_framework import fields
from rest_framework import serializers

from center.serializer import UserSerializer
from .models import *


class CustomMultipleChoiceField(fields.MultipleChoiceField):
    def to_representation(self, value):
        return list(super().to_representation(value))


class RoomSerializer(serializers.ModelSerializer):
    groups_count = serializers.SerializerMethodField()

    def get_groups_count(self, obj):
        return obj.group_count

    class Meta:
        model = Room
        fields = ['id', 'name', 'groups_count']
        read_only_fields = ['id', 'groups_count']


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'
        depth = 1


class EmpTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpType
        fields = ['role']
        depth = 1


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'role', 'name', 'course', 'phone', 'added']


class GroupSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Groups
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)
    depth = 1

    def get_groups(self, obj):
        return obj.groups

    def get_groups_name(self, obj):
        return obj.groups.name

    class Meta:
        model = Course
        fields = ['id', 'name', 'cost', 'groups']
        read_only_fields = ['id', 'groups']
