from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class Experience(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='experiences'
    )
    position = models.CharField(max_length=150, verbose_name="Poste / Intitulé")
    company = models.CharField(max_length=150, verbose_name="Entreprise / Organisation")
    location = models.CharField(max_length=100, blank=True, verbose_name="Localisation")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    is_current = models.BooleanField(default=False, verbose_name="Poste actuel")
    description = models.TextField(blank=True, verbose_name="Description des responsabilités et accomplissements")
    technologies_used = models.JSONField(
        default=list,
        blank=True,
        help_text="Liste des technologies clés utilisées, ex: ['Django', 'React', 'Docker']"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Expérience professionnelle"
        verbose_name_plural = "Expériences professionnelles"
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.position} chez {self.company} ({self.user.username})"
