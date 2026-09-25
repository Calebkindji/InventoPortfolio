from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.core.validators import FileSizeValidator, validate_image_extension


class Project(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Brouillon'
        IN_PROGRESS = 'IN_PROGRESS', 'En développement'
        COMPLETED = 'COMPLETED', 'Terminé'
        ARCHIVED = 'ARCHIVED', 'Archivé'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    title = models.CharField(max_length=150, verbose_name="Titre du projet")
    short_description = models.CharField(
        max_length=300,
        verbose_name="Description courte / Résumé"
    )
    detailed_description = models.TextField(
        blank=True,
        verbose_name="Description détaillée"
    )
    main_image = models.ImageField(
        upload_to='projects/covers/',
        null=True,
        blank=True,
        validators=[FileSizeValidator(5), validate_image_extension],
        verbose_name="Image principale"
    )
    category = models.CharField(
        max_length=80,
        default="Web",
        verbose_name="Catégorie (Web, Mobile, Design, Open Source, etc.)"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Statut du projet"
    )
    progress_percentage = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Progression (%)"
    )
    technologies_used = models.JSONField(
        default=list,
        blank=True,
        help_text="Champ conservé pour compatibilité; utiliser ProjectSkill pour les compétences."
    )
    # Champs conservés pour compatibilité avec les clients existants.
    # Les nouveaux liens doivent utiliser ExternalLink.
    github_url = models.URLField(blank=True, verbose_name="Lien GitHub")
    gitlab_url = models.URLField(blank=True, verbose_name="Lien GitLab")
    demo_url = models.URLField(blank=True, verbose_name="Lien de démonstration")
    app_url = models.URLField(blank=True, verbose_name="Lien vers l'application")
    documentation_url = models.URLField(blank=True, verbose_name="Lien de la documentation")
    video_url = models.URLField(blank=True, verbose_name="Lien de la vidéo")
    start_date = models.DateField(null=True, blank=True, verbose_name="Date de début")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    role = models.CharField(max_length=150, blank=True, verbose_name="Rôle dans le projet")
    is_featured = models.BooleanField(default=False, verbose_name="Mettre en avant sur le portfolio")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['order', '-updated_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()}) - {self.user.username}"


class ProjectSkill(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_skills'
    )
    skill = models.ForeignKey(
        'skills.Skill',
        on_delete=models.CASCADE,
        related_name='project_skills'
    )

    class Meta:
        verbose_name = "Compétence de projet"
        verbose_name_plural = "Compétences de projet"
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'skill'],
                name='unique_project_skill'
            )
        ]

    def __str__(self):
        return f"{self.project.title} - {self.skill.name}"


class ExternalLink(TimeStampedModel):
    class LinkType(models.TextChoices):
        GITHUB = 'GITHUB', 'GitHub'
        GITLAB = 'GITLAB', 'GitLab'
        DEMO = 'DEMO', 'Démonstration'
        WEBSITE = 'WEBSITE', 'Site web'
        LINKEDIN = 'LINKEDIN', 'LinkedIn'
        DOCUMENTATION = 'DOCUMENTATION', 'Documentation'
        VIDEO = 'VIDEO', 'Vidéo'
        OTHER = 'OTHER', 'Autre'

    profile = models.ForeignKey(
        'profiles.UserProfile',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='external_links'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='external_links'
    )
    url = models.URLField(max_length=500)
    label = models.CharField(max_length=120)
    type = models.CharField(
        max_length=30,
        choices=LinkType.choices,
        default=LinkType.OTHER
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Lien externe"
        verbose_name_plural = "Liens externes"
        ordering = ['order', 'created_at']
        constraints = [
            models.CheckConstraint(
                condition=(
                    (models.Q(profile__isnull=False) & models.Q(project__isnull=True)) |
                    (models.Q(profile__isnull=True) & models.Q(project__isnull=False))
                ),
                name='external_link_single_owner'
            )
        ]

    def __str__(self):
        return self.label


class Media(TimeStampedModel):
    class MediaType(models.TextChoices):
        IMAGE = 'IMAGE', 'Image'
        VIDEO = 'VIDEO', 'Vidéo'
        DOCUMENT = 'DOCUMENT', 'Document'

    storage_key = models.CharField(max_length=500, unique=True)
    url = models.URLField(max_length=1000, blank=True)
    mime_type = models.CharField(max_length=100)
    size = models.PositiveBigIntegerField(default=0)
    alt_text = models.CharField(max_length=255, blank=True)
    media_type = models.CharField(
        max_length=20,
        choices=MediaType.choices,
        default=MediaType.IMAGE
    )

    class Meta:
        verbose_name = "Média"
        verbose_name_plural = "Médias"

    def __str__(self):
        return self.storage_key


class ProjectMedia(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='media_gallery'
    )
    media = models.ForeignKey(
        Media,
        on_delete=models.CASCADE,
        related_name='project_media'
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Média de projet"
        verbose_name_plural = "Médias de projets"
        ordering = ['order', 'created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['project', 'media'],
                name='unique_project_media'
            )
        ]

    def __str__(self):
        return f"Média pour {self.project.title} (#{self.id})"
