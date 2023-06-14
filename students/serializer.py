import datetime

from rest_framework import serializers

from center.serializer import UserSerializer
from courses.models import *
from .models import Davomat


class Davomatserializer(serializers.ModelSerializer):
    class Meta:
        model = Davomat
        fields = '__all__'
        depth = 1


class StudentSerializer(serializers.ModelSerializer):
    davomat = Davomatserializer(many=True, read_only=True)
    groups = serializers.SerializerMethodField()
    classes = serializers.SerializerMethodField()
    user = UserSerializer()
    payments = serializers.SerializerMethodField()

    def get_groups(self, obj):
        return obj.add_to_group.all().values('id', "name", 'teacher__name')

    def get_classes(self, obj):
        return obj.classes.all().values('id', 'name')

    def get_payments(self, obj):
        groups = obj.add_to_group.all()
        info = []
        for group in groups:
            data = {}
            try:
                group_me = Groups.objects.get(id=group.id)
                try:
                    payment = obj.payment.filter(group=group_me).latest('date')
                    now = datetime.datetime.now(datetime.timezone.utc)
                    day = (now - payment.date).days
                    data['type'] = payment.type
                    data['cost'] = payment.cost
                    data['date'] = payment.date
                    data['user'] = payment.user.username
                    data['description'] = payment.description
                    data['status'] = True if day < 27 else False
                    info.append(data)
                except Exception as e:
                    pass
            except Groups.DoesNotExist:
                pass
        return info

    class Meta:
        model = Student
        fields = "__all__"
        read_only_fields = ['one_id', 'id', 'user', 'first_name', 'last_name', 'groups', 'classes', 'payments']

