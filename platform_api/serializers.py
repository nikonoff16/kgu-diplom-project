from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import DocumentationPage, Subject, Theme, Labwork, DockerContainer, LabTasks
from rest_framework import permissions

from .permissions import InStudentAuthGroup, InTeacherAuthGroup, InAdminAuthGroup


class DocumentSerializer(serializers.ModelSerializer):
    permission_classes = [InStudentAuthGroup, InTeacherAuthGroup, InAdminAuthGroup]
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = DocumentationPage
        fields = ("id", "header", "created", "owner")


class DocumentDetailsSerializer(serializers.ModelSerializer):
    permission_classes = [InTeacherAuthGroup, InAdminAuthGroup]

    class Meta:
        model = DocumentationPage
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Group
        fields = ("id", "name", "users",)


class DockerImageSerializer(serializers.ModelSerializer):
    permission_classes = [InStudentAuthGroup]

    class Meta:
        model = DockerContainer
        fields = "__all__"


class DockerImageDetailsSerializer(serializers.ModelSerializer):
    # permission_classes = [InStudentAuthGroup]

    class Meta:
        model = DockerContainer
        fields = "__all__"


class DockerImageTreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DockerContainer
        fields = "__all__"


class LabTaskSerializer(serializers.ModelSerializer):
    permission_classes = [InStudentAuthGroup]

    class Meta:
        model = LabTasks
        fields = "__all__"


class LabworkSerializer(serializers.ModelSerializer):
    permission_classes = [InStudentAuthGroup]
    dockers = serializers.PrimaryKeyRelatedField(many=True, queryset=DockerContainer.objects.all())
    tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=LabTasks.objects.all())

    class Meta:
        model = Labwork
        fields = ("id", "name", "created", "modified", "url", "dockers", "tasks",)


class LabworkDetailsSerializer(serializers.ModelSerializer):
    permission_classes = [InStudentAuthGroup]

    class Meta:
        model = Labwork
        fields = ("id", "name", "created", "modified", "url", "theme", "description",)


class LabworkTreeSerializer(serializers.ModelSerializer):
    dockers = DockerImageTreeSerializer(many=True, read_only=True)
    tasks = LabTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Labwork
        fields = ("id", "name", "created", "modified", "url", "dockers", "tasks",)


class ThemeSerializer(serializers.ModelSerializer):
    permission_classes = [InStudentAuthGroup]
    labworks = serializers.PrimaryKeyRelatedField(many=True, queryset=Labwork.objects.all())

    class Meta:
        model = Theme
        fields = ("id", "name", "labworks",)


class ThemeDetailsSerializer(serializers.ModelSerializer):
    permission_classes = [InStudentAuthGroup]
    class Meta:
        model = Theme
        fields = ("id", "name", "description", "subject",)


class ThemeTreeSerializer(serializers.ModelSerializer):
    labworks = LabworkTreeSerializer(many=True, read_only=True)

    class Meta:
        model = Theme
        fields = ("id", "name", "labworks",)


class SubjectSerializer(serializers.ModelSerializer):
    permission_classes = [InStudentAuthGroup]
    themes = serializers.PrimaryKeyRelatedField(many=True, queryset=Theme.objects.all())

    class Meta:
        model = Subject
        fields = ("id", "name", "teachers", "themes",)


class SubjectDetailsSerializer(serializers.ModelSerializer):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Subject
        fields = ("id", "name",  "teachers", "description")


class SubjectTreeSerializer(serializers.ModelSerializer):
    themes = ThemeTreeSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ("id", "name",  "teachers", "themes",)


