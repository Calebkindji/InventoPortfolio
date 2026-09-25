from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateContentReportView, AdminReportViewSet, AdminUserViewSet, AdminGlobalStatsView

app_name = 'moderation'

router = DefaultRouter()
router.register(r'admin/reports', AdminReportViewSet, basename='admin-report')
router.register(r'admin/users', AdminUserViewSet, basename='admin-user')

urlpatterns = [
    path('reports/', CreateContentReportView.as_view(), name='create_report'),
    path('admin/stats/', AdminGlobalStatsView.as_view(), name='admin_stats'),
    path('', include(router.urls)),
]
