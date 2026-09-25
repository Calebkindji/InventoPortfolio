from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


username_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_-]+$',
    message="Le nom d'utilisateur ne peut contenir que des lettres, des chiffres, des tirets et des underscores."
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire.")
        if not username:
            raise ValueError("Le nom d'utilisateur est obligatoire.")
        
        email = self.normalize_email(email)
        username = username.lower().strip()
        extra_fields.setdefault('is_active', True)
        
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.Role.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        USER = 'USER', 'Utilisateur'
        ADMIN = 'ADMIN', 'Administrateur'

    email = models.EmailField(unique=True, verbose_name="Adresse e-mail")
    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[username_validator],
        verbose_name="Nom d'utilisateur"
    )
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name="Rôle"
    )
    is_suspended = models.BooleanField(
        default=False,
        verbose_name="Compte suspendu"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def clean(self):
        super().clean()
        if self.username:
            self.username = self.username.lower().strip()

    def __str__(self):
        return f"{self.get_full_name()} (@{self.username})"
