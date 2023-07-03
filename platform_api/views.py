import django_filters
from rest_framework import generics, viewsets
from .models import DocumentationPage, Theme, Subject, Labwork, DockerContainer, LabTasks
from .serializers import DocumentSerializer, DocumentDetailsSerializer, LabTaskSerializer, GroupSerializer
from .serializers import UserSerializer
from .serializers import ThemeSerializer, ThemeDetailsSerializer
from .serializers import SubjectSerializer, SubjectDetailsSerializer
from .serializers import LabworkSerializer, LabworkDetailsSerializer
from .serializers import DockerImageSerializer, DockerImageDetailsSerializer, DockerImageTreeSerializer
from .serializers import SubjectTreeSerializer
from django.contrib.auth.models import User, Group

from django.http import HttpResponse
from wsgiref.util import FileWrapper


class WikiCreate(generics.CreateAPIView):
    queryset = DocumentationPage.objects.all()
    serializer_class = DocumentDetailsSerializer


class WikiestList(generics.ListAPIView):
    queryset = DocumentationPage.objects.all().order_by('id').values()
    serializer_class = DocumentSerializer


class WikiesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DocumentationPage.objects.all()
    serializer_class = DocumentDetailsSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class LabTasksCreate(generics.CreateAPIView):
    queryset = LabTasks.objects.all()
    serializer_class = LabTaskSerializer


class LabTasksList(generics.ListAPIView):
    queryset = LabTasks.objects.all()
    serializer_class = LabTaskSerializer
    ordering_fields = ['teacher']

    def get_queryset(self):
        queryset = LabTasks.objects.all()
        labwork = None
        if 'labwork' in self.kwargs.keys():
            labwork = self.kwargs['labwork']
        teacher = self.request.query_params.get('teacher')

        if teacher is not None:
            queryset = queryset.filter(labwork=labwork, student=teacher)
        elif labwork is not None:
            queryset = queryset.filter(labwork=labwork)

        return queryset


class LabTasksDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LabTasks.objects.all()
    serializer_class = LabTaskSerializer


class LabTasksDownload(generics.ListAPIView):

    def get(self, request, pk=1, format=None):
        queryset = LabTasks.objects.get(id=pk)
        file_handle = queryset.docker_data.path
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/whatever')
        response['Content-Disposition'] = 'attachment; docker_data="%s"' % queryset.docker_data.name
        return response


class LabworkCreate(generics.CreateAPIView):
    queryset = Labwork.objects.all()
    serializer_class = LabworkDetailsSerializer


class LabworkList(generics.ListAPIView):
    queryset = Labwork.objects.all()
    serializer_class = LabworkSerializer


class LabworkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Labwork.objects.all()
    serializer_class = LabworkDetailsSerializer


class DockerImageCreate(generics.CreateAPIView):
    queryset = DockerContainer.objects.all()
    serializer_class = DockerImageDetailsSerializer


class DockerImageList(generics.ListAPIView):
    queryset = DockerContainer.objects.all()
    serializer_class = DockerImageSerializer
    ordering_fields = ['group', 'student']

    def get_queryset(self):
        queryset = DockerContainer.objects.all()
        labwork = None
        if 'labwork' in self.kwargs.keys():
            labwork = self.kwargs['labwork']
        student = self.request.query_params.get('student')

        if student is not None:
            queryset = queryset.filter(labwork=labwork, student=student)
        elif labwork is not None:
            queryset = queryset.filter(labwork=labwork)

        return queryset


class DockerImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DockerContainer.objects.all()
    serializer_class = DockerImageDetailsSerializer


class DockerImageDownload(generics.ListAPIView):

    def get(self, request, pk=1, format=None):
        queryset = DockerContainer.objects.get(id=pk)
        file_handle = queryset.docker_data.path
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/whatever')
        response['Content-Disposition'] = 'attachment; docker_data="%s"' % queryset.docker_data.name
        return response


class ThemeCreate(generics.CreateAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeDetailsSerializer


class ThemeList(generics.ListAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class ThemeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Theme.objects.all()
    serializer_class = ThemeDetailsSerializer


class SubjectCreate(generics.CreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectDetailsSerializer


class SubjectList(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectDetailsSerializer


class TreeView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectTreeSerializer

    def get_queryset(self):
        queryset = Subject.objects.all()
        teachers = self.request.query_params.get('teachers')

        if teachers is not None:
            queryset = queryset.filter(teachers=teachers)

        return queryset
