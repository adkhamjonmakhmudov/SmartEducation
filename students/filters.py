from django_filters import rest_framework as filters
from .models import Student
class StudentFilter(filters.FilterSet):
    added = filters.DateFilter(field_name='added', lookup_expr='added')
    class Meta:
        model = Student
        fields = ['name', 'phone','added']