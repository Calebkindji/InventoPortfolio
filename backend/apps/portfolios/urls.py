from django.urls import path
from .views import (
    PortfolioMeView, PortfolioPublishView, PortfolioUnpublishView,
    PortfolioPreviewView, PublicPortfolioDetailView, CheckSlugAvailabilityView
)

app_name = 'portfolios'

urlpatterns = [
    path('me/', PortfolioMeView.as_view(), name='portfolio_me'),
    path('me/publish/', PortfolioPublishView.as_view(), name='portfolio_publish'),
    path('me/unpublish/', PortfolioUnpublishView.as_view(), name='portfolio_unpublish'),
    path('me/preview/', PortfolioPreviewView.as_view(), name='portfolio_preview'),
    path('check-slug/', CheckSlugAvailabilityView.as_view(), name='check_slug'),
    path('<slug:slug>/', PublicPortfolioDetailView.as_view(), name='public_portfolio'),
]
