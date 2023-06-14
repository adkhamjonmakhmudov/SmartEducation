from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, pagination
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from payment.models import StudentPayment
from .filters import StudentFilter
from .serializer import *

fs = FileSystemStorage(location='tmp/')


class StudentPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50
    queryset = Student.objects.all()
    filterset_class = Student

    def get_paginated_response(self, data):
        return Response({
            'page_size': self.page_size,
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class StudentViewset(ModelViewSet):
    queryset = Student.objects.all()
    pagination_class = StudentPagination
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name', 'phone']
    filterset_class = StudentFilter

    def create(self, request, *args, **kwargs):
        data = request.data
        courses = data.get('add_to_course', [])
        groups = data.get('add_to_group', [])

        student = Student(name=data['name'], phone=data['phone'], user=request.user, added=data.get('added', None))

        with transaction.atomic():
            student.save()

            for course_id in courses:
                try:
                    course = Course.objects.get(id=course_id)
                    student.add_to_course.add(course)
                except ObjectDoesNotExist:
                    return Response(f"Course with ID {course_id} does not exist.", status=status.HTTP_400_BAD_REQUEST)

            student.add_to_group.set(groups)

        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        student_object = self.get_object()
        data = request.data
        student_object.name = data.get('name', student_object.name)
        student_object.phone = data.get('phone', student_object.phone)
        student_object.save()
        serializer = StudentSerializer(student_object)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class DavomatViewset(ModelViewSet):
    queryset = Davomat.objects.all()
    serializer_class = Davomatserializer

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'students' in data:
            for student in data['students']:
                try:
                    talaba = Student.objects.get(id=student['id'])
                    Davomat.objects.create(student=talaba, status=student.get('status', True),
                                           description=student.get('description', 'Sabab korsatilmagan'))
                except Student.DoesNotExist:
                    pass
            return Response("Davomat olindi!")
        else:
            return Response('Student Doesnt Found')

    def partial_update(self, request, *args, **kwargs):
        davomat_data = self.get_object()
        data = request.data
        if 'students' in data:
            for student in data['students']:
                try:
                    student = Student.objects.get(id=student['id'])
                    davomat_data.student = student
                    davomat_data.description = student.get('description', davomat_data.description)
                    davomat_data.status = student.get('status', davomat_data.status)
                    davomat_data.date = student.get('date', davomat_data.date)
                    serializer = Davomatserializer(davomat_data)
                    return Response(serializer.data)
                except Student.DoesNotExist:
                    return Response('Student not found')
        else:
            return Response('student field required')

    def update(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class StudentPaymentInfo(APIView):
    def get(self, request, pk):
        payments = []
        student = Student.objects.get(id=pk)
        payment_students = StudentPayment.objects.filter(student=student)
        for group in student.groups.all():
            payment = payment_students.filter(group=Groups.objects.get(id=group.id)).last()
            if payment is not None:
                info = {}
                info['id'] = payment.id
                info['student_id'] = payment.student.id
                info['student_name'] = payment.student.name
                info['cost'] = payment.cost
                info['date'] = payment.date
                info['group'] = payment.group.name
                info['user'] = payment.user.username
                payments.append(info)
        return Response(payments, status=status.HTTP_200_OK)
