from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.core.validators import FileSizeValidator, validate_document_extension


class Certification(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certifications'
    )
    name = models.CharField(max_length=150, verbose_name="Nom de la certification")
    issuing_organization = models.CharField(max_length=150, verbose_name="Organisme délivreur")
    issue_date = models.DateField(verbose_name="Date d'obtention")
    expiration_date = models.DateField(null=True, blank=True, verbose_name="Date d'expiration")
    credential_id = models.CharField(max_length=100, blank=True, verbose_name="Identifiant de certification")
    credential_url = models.URLField(blank=True, verbose_name="Lien de vérification")
    document = models.FileField(
        upload_to='certifications/documents/',
        null=True,
        blank=True,
        validators=[FileSizeValidator(10), validate_document_extension],
        verbose_name="Document justificatif (PDF)"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ['order', '-issue_date']

    def __str__(self):
        return f"{self.name} - {self.issuing_organization} ({self.user.username})"
