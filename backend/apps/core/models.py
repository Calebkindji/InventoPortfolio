from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base class providing self-updating created_at and updated_at fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    class Meta:
        abstract = True
