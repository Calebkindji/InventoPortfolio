from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class Portfolio(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Brouillon'
        PUBLISHED = 'PUBLISHED', 'Publié'
        ARCHIVED = 'ARCHIVED', 'Archivé'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolio'
    )
    slug = models.SlugField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Slug public"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Statut de publication"
    )
    custom_theme = models.JSONField(
        default=dict,
        blank=True,
        help_text="Configuration visuelle facultative du template"
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de publication"
    )

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolios"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username) or f"portfolio-{self.user_id}"
            candidate = base_slug
            suffix = 2
            Model = type(self)
            while Model.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    @property
    def is_public(self):
        return self.status == self.Status.PUBLISHED and not self.user.is_suspended

    def publish(self):
        self.status = self.Status.PUBLISHED
        self.published_at = timezone.now()
        self.save(update_fields=['status', 'published_at', 'updated_at'])

    def unpublish(self):
        self.status = self.Status.DRAFT
        self.save(update_fields=['status', 'updated_at'])

    def __str__(self):
        return f"Portfolio de {self.user.username} ({self.get_status_display()})"
