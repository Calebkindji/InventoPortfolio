from django.urls import path
from .views import RecordVisitView, RecordProjectView, RecordLinkClickView, AnalyticsDashboardView

app_name = 'analytics'

urlpatterns = [
    path('visit/', RecordVisitView.as_view(), name='record_visit'),
    path('project-view/', RecordProjectView.as_view(), name='record_project_view'),
    path('click/', RecordLinkClickView.as_view(), name='record_click'),
    path('dashboard/', AnalyticsDashboardView.as_view(), name='dashboard'),
]
