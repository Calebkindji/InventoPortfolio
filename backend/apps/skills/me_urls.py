from django.urls import path
from .views import MySkillsView

urlpatterns = [path('', MySkillsView.as_view(), name='my_skills')]
