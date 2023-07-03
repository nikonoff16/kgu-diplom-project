from django.db import models
from django.utils import timezone

import uuid


def get_docker_full_path(test, filename):
    ext = filename.split('.')[-1]
    root = 'import'
    path = f'{root}/submissions'
    name = f'{uuid.uuid4()}'
    return f'{path}/{name}.{ext}'


class DocumentationPage(models.Model):
    owner = models.ForeignKey('auth.User', default=1, related_name='documents', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    header = models.TextField(default='Пустой заголовок')
    content = models.TextField(default='')

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True


class Subject(models.Model):
    name = models.TextField(default="Новый предмет")
    description = models.TextField(default='Описание')
    teachers = models.TextField(default='')

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True


class Theme(models.Model):
    subject = models.ForeignKey('Subject', related_name='themes', on_delete=models.CASCADE)
    name = models.TextField(default="Новая тема")
    description = models.TextField(default='Описание')

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True


class Labwork(models.Model):
    name = models.TextField(default='Новая лабка')
    theme = models.ForeignKey('Theme', related_name='labworks', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    url = models.TextField(default='Пустой заголовок')
    description = models.TextField(default='Описание')

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True


class DockerContainer(models.Model):
    labwork = models.ForeignKey(Labwork, related_name='dockers', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    student = models.TextField(default='')
    student_name = models.TextField(default='')
    group = models.TextField(default='')
    docker_data = models.FileField(upload_to=get_docker_full_path, blank=True)
    mark = models.IntegerField(default=2)

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True


class LabTasks(models.Model):
    labwork = models.ForeignKey(Labwork, related_name='tasks', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    teacher = models.TextField(default='')
    docker_data = models.FileField(upload_to=get_docker_full_path, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = True