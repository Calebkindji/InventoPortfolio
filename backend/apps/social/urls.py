from django.urls import path
from .views import ToggleProjectLikeView, ProjectCommentViewSet, ToggleFollowView, NotificationListView

app_name = 'social'

comment_list = ProjectCommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

comment_detail = ProjectCommentViewSet.as_view({
    'get': 'retrieve',
    'delete': 'destroy'
})

urlpatterns = [
    path('projects/<int:project_id>/like/', ToggleProjectLikeView.as_view(), name='toggle_project_like'),
    path('projects/<int:project_id>/comments/', comment_list, name='project_comments'),
    path('comments/<int:pk>/', comment_detail, name='comment_detail'),
    path('users/<int:user_id>/follow/', ToggleFollowView.as_view(), name='toggle_follow'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
]
