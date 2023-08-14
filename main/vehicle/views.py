import stripe
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from main.vehicle.models import Course, Lesson, Payment, CourseSubscription
from main.vehicle.paginators import VehiclePaginator
from main.vehicle.permissions import IsOwnerOrStaff
from main.vehicle.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, LessonPaymentSerializer, \
    LessonCreateSerializer, CourseCreateSerializer, SubscriptionSerializer


class CourseViewSet(ModelViewSet):  # все для ViewSet
    """Course View"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [AllowAny]  # для не автор пользователей этого видно не будет(ошибка по выводу инфы)
    pagination_class = VehiclePaginator  # Пагинация

    # def post(self, *args, **kwargs):  # во ViewSet пост отвечает за создание
    #     self.serializer_class = CourseCreateSerializer  # Это ViewSet тоже-самое что и с LessonCreateAPIView
    #     super()


class LessonCreateAPIView(generics.CreateAPIView):  # все для Generic
    """Create Lesson"""
    serializer_class = LessonCreateSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):  # сохранения нового владельца при создании нового урока
        mew_lesson = serializer.save()
        mew_lesson.owner = self.request.user  # owner - владелец  (нужно добавить в models)
        mew_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Lesson List"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]
    pagination_class = VehiclePaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Lesson Retrive"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Lesson Updaate"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Lesson Delete"""
    queryset = Lesson.objects.all()
    permission_classes = [AllowAny]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Payment Create"""
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]


class PaymentListAPIView(generics.ListAPIView):  # Фильтр
    """Payment List"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson")
    ordering_fields = ("payment_date",)
    pagination_class = VehiclePaginator


class LessonPaymentAPIView(generics.ListAPIView):
    """Lesson Pyment"""
    serializer_class = LessonPaymentSerializer
    queryset = Payment.objects.filter(lesson__isnull=False)  # уроки должны быть заполненны
    pagination_class = VehiclePaginator
    # permission_classes = [AllowAny]


class SubscribeCourseAPIView(generics.ListAPIView):
    """Create Subscribe"""
    def post(self, request, course_id):
        user = request.user
        course = Course.objects.get(id=course_id)
        if not course:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        subscription, created = CourseSubscription.objects.get_or_create(user=user, course=course)
        subscription.is_subscribed = True
        subscription.save()
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)


class UnsubscribeCourseAPIView(generics.ListAPIView):
    """Delete Subscribe"""
    def delete(self, request, course_id):
        user = request.user
        course = Course.objects.get(id=course_id)
        if not course:
            return Response({'error': 'Курс не найден'}, status=status.HTTP_404_NOT_FOUND)
        subscription = CourseSubscription.objects.filter(user=user, course=course).first()
        if not subscription:
            return Response({'error': 'Подписка не найдена'}, status=status.HTTP_404_NOT_FOUND)
        subscription.is_subscribed = False
        subscription.save()
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

class SubscrubeRetrieveAPIView(generics.RetrieveAPIView):
    """Subscribe Retrive"""
    serializer_class = SubscriptionSerializer
    queryset = CourseSubscription.objects.all()
    permission_classes = [AllowAny]

