from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.core.health import LiveHealthView, ReadyHealthView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('health/live/', LiveHealthView.as_view(), name='health-live'),
    path('health/ready/', ReadyHealthView.as_view(), name='health-ready'),
    path('admin/', admin.site.urls),

    # API v1 Endpoints
    path('api/v1/auth/', include('apps.accounts.urls', namespace='accounts')),
    path('api/v1/profiles/', include('apps.profiles.urls', namespace='profiles')),
    path('api/v1/skills/', include('apps.skills.urls', namespace='skills')),
    path('api/v1/experiences/', include('apps.experiences.urls', namespace='experiences')),
    path('api/v1/educations/', include('apps.educations.urls', namespace='educations')),
    path('api/v1/certifications/', include('apps.certifications.urls', namespace='certifications')),
    path('api/v1/projects/', include('apps.projects.urls', namespace='projects')),
    path('api/v1/portfolios/', include('apps.portfolios.urls', namespace='portfolios')),
    path('api/v1/explore/', include('apps.exploration.urls', namespace='exploration')),
    path('api/v1/analytics/', include('apps.analytics.urls', namespace='analytics')),
    path('api/v1/moderation/', include('apps.moderation.urls', namespace='moderation')),
    path('api/v1/social/', include('apps.social.urls', namespace='social')),
    path('api/v1/exports/', include('apps.exports.urls', namespace='exports')),

    # Documentation Swagger / OpenAPI v3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
