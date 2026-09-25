from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class SkillCategory(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "Catégorie de compétence"
        verbose_name_plural = "Catégories de compétences"
        ordering = ['name']

    def __str__(self):
        return self.name


class Skill(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la compétence")
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='skills',
        verbose_name="Catégorie"
    )

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"
        ordering = ['name']

    def __str__(self):
        return self.name


class ProfileSkill(TimeStampedModel):
    class SkillLevel(models.TextChoices):
        BEGINNER = 'BEGINNER', 'Débutant'
        INTERMEDIATE = 'INTERMEDIATE', 'Intermédiaire'
        ADVANCED = 'ADVANCED', 'Avancé'
        EXPERT = 'EXPERT', 'Expert'

    profile = models.ForeignKey(
        'profiles.UserProfile',
        on_delete=models.CASCADE,
        related_name='profile_skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='profile_skills'
    )
    level = models.CharField(
        max_length=20,
        choices=SkillLevel.choices,
        default=SkillLevel.INTERMEDIATE
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Compétence du profil"
        verbose_name_plural = "Compétences du profil"
        ordering = ['order', 'skill__name']
        constraints = [
            models.UniqueConstraint(
                fields=['profile', 'skill'],
                name='unique_profile_skill'
            )
        ]

    def __str__(self):
        return f"{self.profile.user.username} - {self.skill.name} ({self.get_level_display()})"
