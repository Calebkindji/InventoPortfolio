from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class ContentReport(TimeStampedModel):
    class TargetType(models.TextChoices):
        PROFILE = 'PROFILE', 'Profil'
        PORTFOLIO = 'PORTFOLIO', 'Portfolio'
        PROJECT = 'PROJECT', 'Projet'
        IMAGE = 'IMAGE', 'Image / Média'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        REVIEWED = 'REVIEWED', 'En cours d\'examen'
        RESOLVED = 'RESOLVED', 'Traité'
        DISMISSED = 'DISMISSED', 'Rejeté'

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='submitted_reports'
    )
    target_type = models.CharField(
        max_length=20,
        choices=TargetType.choices,
        verbose_name="Type d'élément"
    )
    target_id = models.PositiveIntegerField(verbose_name="Identifiant de l'élément")
    reason = models.TextField(verbose_name="Motif du signalement")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Statut du traitement"
    )
    admin_notes = models.TextField(blank=True, verbose_name="Notes de modération")

    class Meta:
        verbose_name = "Signalement de contenu"
        verbose_name_plural = "Signalements de contenus"
        ordering = ['-created_at']

    def __str__(self):
        return f"Signalement #{self.id} ({self.get_target_type_display()} #{self.target_id})"
