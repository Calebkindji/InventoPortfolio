from django.urls import path
from .views import ExplorePortfoliosView, ExploreProjectsView, GlobalSearchView

app_name = 'exploration'

urlpatterns = [
    path('portfolios/', ExplorePortfoliosView.as_view(), name='explore_portfolios'),
    path('projects/', ExploreProjectsView.as_view(), name='explore_projects'),
    path('search/', GlobalSearchView.as_view(), name='global_search'),
]
