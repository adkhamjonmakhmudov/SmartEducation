from django.urls import path, include
from rest_framework.routers import DefaultRouter

from courses.views import *
from payment.views import *
from students.views import *
from .views import *

router = DefaultRouter()
router.register('director', DirectorViewset, basename='director')
router.register('manager', ManagerViewset)
router.register('employee', EmployeeViewset)
router.register('emptype', EmpTypeViewset)
router.register('course', CourseViewset)
router.register('students', StudentViewset, basename='students')
router.register('rooms', RoomViewset)
router.register('groups', GroupsViewset)
router.register('davomat', DavomatViewset)
router.register('payment', StudentPaymentViewset)
router.register('output-payment', OutputPaymentViewset)
router.register('classroom', ClassRoomViewset)
urlpatterns = [
    path('', include(router.urls)),
    path('info/<int:pk>/', StudentPaymentInfo.as_view()),
    path('paymenttype/', PaymentAbout.as_view()),
    path('outputpaymenttype/', OutputPaymentAbout.as_view())

]
