from django.db import models
from apps.portfolios.models import Portfolio
from apps.projects.models import Project


class PortfolioVisit(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='visits'
    )
    visited_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    referrer = models.URLField(blank=True, max_length=500)
    user_agent = models.TextField(blank=True)

    class Meta:
        verbose_name = "Visite de portfolio"
        verbose_name_plural = "Visites de portfolios"
        ordering = ['-visited_at']


class ProjectView(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='views'
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Vue de projet"
        verbose_name_plural = "Vues de projets"
        ordering = ['-viewed_at']


class LinkClick(models.Model):
    class LinkType(models.TextChoices):
        GITHUB = 'GITHUB', 'GitHub'
        GITLAB = 'GITLAB', 'GitLab'
        DEMO = 'DEMO', 'Démonstration'
        WEBSITE = 'WEBSITE', 'Site Personnel'
        LINKEDIN = 'LINKEDIN', 'LinkedIn'
        OTHER = 'OTHER', 'Autre'

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='link_clicks'
    )
    link_type = models.CharField(
        max_length=20,
        choices=LinkType.choices,
        default=LinkType.OTHER
    )
    target_url = models.URLField(max_length=500)
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Clic sur lien"
        verbose_name_plural = "Clics sur liens"
        ordering = ['-clicked_at']
