from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from apps.portfolios.models import Portfolio
from apps.portfolios.serializers import PublicPortfolioSerializer
from apps.projects.models import Project
from apps.projects.serializers import ProjectSerializer


class ExplorePortfoliosView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PublicPortfolioSerializer
    pagination_class = None  # DRF global pagination is enabled; keep response contract simple below.

    def get_queryset(self):
        qs = Portfolio.objects.filter(
            status=Portfolio.Status.PUBLISHED,
            user__is_suspended=False
        ).select_related('user', 'user__profile').distinct()
        q = self.request.query_params.get('q', '').strip()
        skill = self.request.query_params.get('skill', '').strip()
        category = self.request.query_params.get('category', '').strip()
        sort = self.request.query_params.get('sort', 'recent')
        if q:
            qs = qs.filter(
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(user__username__icontains=q) |
                Q(user__profile__title__icontains=q) |
                Q(user__profile__bio__icontains=q)
            )
        if skill:
            qs = qs.filter(user__profile__profile_skills__skill__name__iexact=skill)
        if category:
            qs = qs.filter(user__profile__profile_skills__skill__category__slug=category)
        ordering = {'recent': '-published_at', 'oldest': 'published_at', 'name': 'user__username'}
        return qs.order_by(ordering.get(sort, '-published_at'))


class ExploreProjectsView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        filter_type = self.request.query_params.get('type', 'all')
        qs = Project.objects.filter(user__portfolio__status=Portfolio.Status.PUBLISHED, user__is_suspended=False).exclude(status='ARCHIVED')

        if filter_type == 'recent':
            return qs.order_by('-created_at')
        elif filter_type == 'in_progress':
            return qs.filter(status=Project.Status.IN_PROGRESS)
        elif filter_type == 'featured':
            return qs.filter(is_featured=True)
        return qs.order_by('-updated_at')


class GlobalSearchView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'portfolios': [], 'projects': []})

        portfolios = Portfolio.objects.filter(
            status=Portfolio.Status.PUBLISHED,
            user__is_suspended=False
        ).filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__profile__title__icontains=query) |
            Q(user__profile__bio__icontains=query) |
            Q(user__profile__profile_skills__skill__name__icontains=query)
        ).distinct()[:10]

        projects = Project.objects.filter(
            user__portfolio__status=Portfolio.Status.PUBLISHED,
            user__is_suspended=False
        ).filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__icontains=query)
        ).distinct()[:10]

        return Response({
            'query': query,
            'portfolios': PublicPortfolioSerializer(portfolios, many=True, context={'request': request}).data,
            'projects': ProjectSerializer(projects, many=True, context={'request': request}).data,
        })
