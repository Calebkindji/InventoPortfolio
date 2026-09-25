from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class Education(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='educations'
    )
    institution = models.CharField(max_length=150, verbose_name="Établissement")
    degree = models.CharField(max_length=150, verbose_name="Diplôme / Titre obtenu")
    field_of_study = models.CharField(max_length=150, blank=True, verbose_name="Domaine d'études")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    description = models.TextField(blank=True, verbose_name="Description / Projets académiques")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.degree} à {self.institution} ({self.user.username})"
