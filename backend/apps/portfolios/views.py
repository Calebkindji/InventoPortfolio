from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from .models import Portfolio
from .serializers import PortfolioStateSerializer, PublicPortfolioSerializer
from .services import PortfolioPublicationService

User = get_user_model()


class PortfolioMeView(generics.RetrieveUpdateAPIView):
    serializer_class = PortfolioStateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        portfolio, _ = Portfolio.objects.get_or_create(user=self.request.user)
        return portfolio

    def perform_update(self, serializer):
        serializer.save()


class PortfolioPublishView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PortfolioStateSerializer

    def post(self, request, *args, **kwargs):
        portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
        PortfolioPublicationService(portfolio).publish()
        return Response(PortfolioStateSerializer(portfolio).data, status=status.HTTP_200_OK)


class PortfolioUnpublishView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PortfolioStateSerializer

    def post(self, request, *args, **kwargs):
        portfolio, _ = Portfolio.objects.get_or_create(user=request.user)
        portfolio.unpublish()
        return Response(PortfolioStateSerializer(portfolio).data, status=status.HTTP_200_OK)


class PortfolioPreviewView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PublicPortfolioSerializer

    def get_object(self):
        portfolio, _ = Portfolio.objects.get_or_create(user=self.request.user)
        return Portfolio.objects.select_related('user', 'user__profile').prefetch_related(
            'user__profile__profile_skills__skill__category',
            'user__experiences',
            'user__educations',
            'user__certifications',
            'user__projects'
        ).get(pk=portfolio.pk)


class CheckSlugAvailabilityView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        slug = request.query_params.get('slug', '').strip().lower()
        if not slug:
            return Response({'detail': 'Le paramètre slug est obligatoire.'}, status=status.HTTP_400_BAD_REQUEST)

        normalized_slug = slugify(slug)
        if not normalized_slug:
            return Response({
                'slug': slug,
                'is_available': False,
                'reason': 'Slug invalide.'
            }, status=status.HTTP_200_OK)

        exists = Portfolio.objects.filter(slug=normalized_slug).exists()
        current_user_portfolio = None
        if request.user and request.user.is_authenticated:
            current_user_portfolio = Portfolio.objects.filter(user=request.user).first()

        if exists and (not current_user_portfolio or current_user_portfolio.slug != normalized_slug):
            return Response({
                'slug': normalized_slug,
                'is_available': False,
                'reason': 'Ce slug est déjà utilisé par un autre portfolio.'
            }, status=status.HTTP_200_OK)

        return Response({
            'slug': normalized_slug,
            'is_available': True,
            'reason': 'Ce slug est disponible.'
        }, status=status.HTTP_200_OK)


class PublicPortfolioDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = PublicPortfolioSerializer

    def get_object(self):
        slug = self.kwargs.get('slug', '').strip().lower()
        return get_object_or_404(
            Portfolio.objects.select_related('user', 'user__profile').prefetch_related(
                'user__profile__profile_skills__skill__category',
                'user__experiences',
                'user__educations',
                'user__certifications',
                'user__projects'
            ),
            slug=slug,
            status=Portfolio.Status.PUBLISHED,
            user__is_suspended=False
        )
