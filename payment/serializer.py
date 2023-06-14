from rest_framework import serializers
from .models import StudentPayment,OutputPayment
class StudentPaymentSerializer(serializers.ModelSerializer):
    sana =  serializers.SerializerMethodField()
    user = serializers.StringRelatedField()
    student = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    def get_student(self,obj):
        return obj.student.name
    def get_group(self,obj):
        return obj.group.name
    def get_sana(self,obj):
        return (obj.date).strftime('%d %b, %Y')
    class Meta:
        model = StudentPayment
        fields = '__all__'
        depth=1
class OutputPaymentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    def get_user(self,obj):
        data = {}
        data['user'] = obj.user.username
        data['role'] = obj.user.role
        return data
    class Meta:
        model = OutputPayment
        fields  = '__all__'
        depth=1
