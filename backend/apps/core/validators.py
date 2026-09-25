import os
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class FileSizeValidator:
    def __init__(self, max_size_mb=5):
        self.max_size_mb = max_size_mb

    def __call__(self, file):
        filesize = file.size
        if filesize > self.max_size_mb * 1024 * 1024:
            raise ValidationError(f"La taille maximale autorisée pour les fichiers est de {self.max_size_mb} MB.")

    def __eq__(self, other):
        return isinstance(other, FileSizeValidator) and self.max_size_mb == other.max_size_mb


def validate_image_extension(file):
    """
    Validates that the file has an image extension (jpg, jpeg, png, webp, gif, svg).
    """
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg']
    if ext not in valid_extensions:
        raise ValidationError(f"Format de fichier non supporté ({ext}). Formats autorisés : {', '.join(valid_extensions)}.")


def validate_document_extension(file):
    """
    Validates document file extension (pdf).
    """
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.pdf']
    if ext not in valid_extensions:
        raise ValidationError(f"Format de document non supporté ({ext}). Formats autorisés : {', '.join(valid_extensions)}.")
