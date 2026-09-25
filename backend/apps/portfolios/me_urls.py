from django.urls import path
from .views import (
    PortfolioMeView,
    PortfolioPublishView,
    PortfolioUnpublishView,
    PortfolioPreviewView,
)

urlpatterns = [
    path('', PortfolioMeView.as_view(), name='portfolio_me'),
    path('publish/', PortfolioPublishView.as_view(), name='portfolio_publish'),
    path('unpublish/', PortfolioUnpublishView.as_view(), name='portfolio_unpublish'),
    path('preview/', PortfolioPreviewView.as_view(), name='portfolio_preview'),
]
