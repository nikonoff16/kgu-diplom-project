from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from .views import WikiestList, WikiesDetail, WikiCreate
from .views import UserViewSet, GroupViewSet
from .views import SubjectList, SubjectDetail, SubjectCreate, TreeView
from .views import ThemeList, ThemeDetail, ThemeCreate
from .views import LabworkList,  LabworkDetail,  LabworkCreate
from .views import LabTasksCreate, LabTasksDetail, LabTasksList, LabTasksDownload
from .views import DockerImageCreate, DockerImageDetail, DockerImageList, DockerImageDownload

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
router.register(r'groups', GroupViewSet, basename="groups")

urlpatterns = [
    path('', include(router.urls)),

    path('tree/', TreeView.as_view(), name='tree-list'),

    path('subjects/new/', SubjectCreate.as_view(), name='subjects-create'),
    path('subjects/', SubjectList.as_view(), name='subjects-list'),
    path('subjects/<int:pk>/', SubjectDetail.as_view(), name='subjects-detail'),

    path('themes/new/', ThemeCreate.as_view(), name='themes-create'),
    path('themes/', ThemeList.as_view(), name='themes-list'),
    path('themes/<int:pk>/', ThemeDetail.as_view(), name='themes-detail'),

    path('labworks/new/', LabworkCreate.as_view(), name='labworks-create'),
    path('labworks/', LabworkList.as_view(), name='labworks-list'),
    path('labworks/<int:pk>/', LabworkDetail.as_view(), name='labworks-detail'),

    path('dockers/new/', DockerImageCreate.as_view(), name='dockers-create'),
    path('dockers/', DockerImageList.as_view(), name='dockers-list'),
    re_path('^dockers/bylab/(?P<labwork>.+)/$', DockerImageList.as_view(), name='dockers-labworks-list'),
    path('dockers/<int:pk>/', DockerImageDetail.as_view(), name='dockers-detail'),
    path('dockers/<int:pk>/download', DockerImageDownload.as_view(), name='dockers-download'),

    path('labtasks/new/', LabTasksCreate.as_view(), name='labtasks-create'),
    path('labtasks/', LabTasksList.as_view(), name='dockers-list'),
    re_path('^labtasks/bylab/(?P<labwork>.+)/$', DockerImageList.as_view(), name='labtasks-labworks-list'),
    path('labtasks/<int:pk>/', LabTasksDetail.as_view(), name='labtasks-detail'),
    path('labtasks/<int:pk>/download', LabTasksDownload.as_view(), name='labtasks-download'),

    path('wikies/new/', WikiCreate.as_view(), name='wikies-create'),
    path('wikies/', WikiestList.as_view(), name='wikies-list'),
    path('wikies/<int:pk>/', WikiesDetail.as_view(), name='wikies-detail'),

    re_path(r'^oidc/', include('keycloak_oidc.urls')),
]
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
