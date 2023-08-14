from django.urls import path

from main.vehicle import views
from main.vehicle.apps import VehicleConfig
from rest_framework.routers import DefaultRouter

from main.vehicle.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentCreateAPIView, LessonPaymentAPIView, PaymentListAPIView, \
    SubscribeCourseAPIView, UnsubscribeCourseAPIView, SubscrubeRetrieveAPIView

# все для ViewSet
app_name = VehicleConfig.name

router = DefaultRouter()
router.register(r"Course", CourseViewSet, basename="course")

# все для Generic
urlpatterns = [
    #
    path('Lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('Lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path("Lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-get"),
    path("Lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("Lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson-delete"),

    # Payment
    path("Payment/", PaymentListAPIView.as_view(), name="payment-list"),
    path("Payment/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("Lesson/Payment/", LessonPaymentAPIView.as_view(), name="lesson-payment"),
    path('Courses/<int:course_id>/subscribe/', SubscribeCourseAPIView.as_view(), name="subscribe"),
    path('Сourses/<int:course_id>/unsubscribe/', UnsubscribeCourseAPIView.as_view(), name="unsubscribe"),
    path("Сourses/<int:pk>/", SubscrubeRetrieveAPIView.as_view(), name="subscribe-get"),

] + router.urls

