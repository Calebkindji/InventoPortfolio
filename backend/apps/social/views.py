from rest_framework import generics, permissions, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import ProjectLike, ProjectComment, Follow, Notification
from .serializers import ProjectCommentSerializer, NotificationSerializer
from apps.projects.models import Project

User = get_user_model()


class ToggleProjectLikeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, project_id, *args, **kwargs):
        project = get_object_or_404(Project, id=project_id)
        user = request.user

        like, created = ProjectLike.objects.get_or_create(user=user, project=project)
        if not created:
            like.delete()
            is_liked = False
            message = "Like retiré."
        else:
            is_liked = True
            message = "Projet aimé !"
            # Create Notification if not liking own project
            if project.user != user:
                Notification.objects.create(
                    recipient=project.user,
                    sender=user,
                    notification_type=Notification.NotificationType.LIKE,
                    message=f"{user.get_full_name()} a aimé votre projet '{project.title}'",
                    target_url=f"/u/{project.user.username}"
                )

        total_likes = project.likes.count()
        return Response({
            "is_liked": is_liked,
            "total_likes": total_likes,
            "message": message
        }, status=status.HTTP_200_OK)


class ProjectCommentViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        if project_id:
            return ProjectComment.objects.filter(project_id=project_id)
        return ProjectComment.objects.all()

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        comment = serializer.save(user=self.request.user, project=project)

        # Notify project owner
        if project.user != self.request.user:
            Notification.objects.create(
                recipient=project.user,
                sender=self.request.user,
                notification_type=Notification.NotificationType.COMMENT,
                message=f"{self.request.user.get_full_name()} a commenté votre projet '{project.title}'",
                target_url=f"/u/{project.user.username}"
            )


class ToggleFollowView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, user_id, *args, **kwargs):
        target_user = get_object_or_404(User, id=user_id)
        user = request.user

        if user == target_user:
            return Response({"detail": "Vous ne pouvez pas vous suivre vous-même."}, status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.get_or_create(follower=user, followed=target_user)
        if not created:
            follow.delete()
            is_following = False
            message = f"Vous ne suivez plus @{target_user.username}."
        else:
            is_following = True
            message = f"Vous suivez maintenant @{target_user.username}."
            # Create Notification
            Notification.objects.create(
                recipient=target_user,
                sender=user,
                notification_type=Notification.NotificationType.FOLLOW,
                message=f"{user.get_full_name()} s'est abonné à votre profil",
                target_url=f"/u/{user.username}"
            )

        followers_count = target_user.followers.count()
        return Response({
            "is_following": is_following,
            "followers_count": followers_count,
            "message": message
        }, status=status.HTTP_200_OK)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Mark unread notifications as read
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return response
