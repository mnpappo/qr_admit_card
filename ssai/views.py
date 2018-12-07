from django.shortcuts import render

from django.http import HttpResponse

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, StudentInfoSerializer
from django.views.generic import ListView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.decorators import action
from django.http import Http404



from .models import StudentInfo


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class StudentInfoListView(generics.ListAPIView):
    queryset = StudentInfo.objects.all()
    serializer_class = StudentInfoSerializer

class StudentInfoViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):

    serializer_class = StudentInfoSerializer
    queryset = StudentInfo.objects.all()
    lookup_field = 'id'


def qr_to_admit_page(request, student_id):
    try:
        student_info = StudentInfo.objects.get(pk=student_id)
    except StudentInfo.DoesNotExist:
        raise Http404("Student Info does not exist")
    context = {'student_info': student_info}
    return render(request, 'index.html', context)