from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="ITG Container Platform API",
        default_version='v1',
        description="Документация REST-интерфейсов сервиса контейнеризированных приложений by ITG-team",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="v.osipov08@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    # url=f'{settings.APP_URL}/api/v3/',
    patterns=[
              path('api/front/', include('platform_api.urls'))],
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path(
        'swagger-ui/',
        TemplateView.as_view(
            template_name='swaggerui/swaggerui.html',
            extra_context={'schema_url': 'openapi-schema'}
        ),
        name='swagger-ui'),
    url(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^oidc/', include('keycloak_oidc.urls')),
    path('api/front/', include('platform_api.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/swagger-ui/', permanent=True))
]