from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import CourseCategory,Course, CourseChapter
from .serializers import CourseCategoryModelSerializer, CourseModelSerializer, CourseRetrieveModelSerializer, CourseChapterSerializer
from .pagination import CourseListPageNumberPagination


class CourseCategoryListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True, is_deleted=False).order_by('orders','-id')
    serializer_class = CourseCategoryModelSerializer


class CourseListAPIView(ListAPIView):
    """课程列表API接口"""
    queryset = Course.objects.filter(is_deleted=False, is_show=True).order_by('orders', 'id')
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('course_category',)
    ordering_fields = ['id', 'students', 'price']
    # 指定分页器
    pagination_class = CourseListPageNumberPagination


"""
/course/(?P<pk>\d+)/
"""
class CourseRetrieveAPIView(RetrieveAPIView):
    """课程详情API接口"""
    queryset = Course.objects.filter(is_show=True, is_deleted=False)
    serializer_class = CourseRetrieveModelSerializer


class CourseChapterListAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_deleted=False, is_show=True).order_by('chapter')
    serializer_class = CourseChapterSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course', ]

