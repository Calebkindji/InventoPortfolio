from rest_framework.exceptions import ValidationError
from .models import Portfolio
from apps.projects.models import Project


class PortfolioPublicationService:
    """Centralise les règles métier de publication du portfolio."""

    def __init__(self, portfolio):
        self.portfolio = portfolio

    def validate(self):
        user = self.portfolio.user
        profile = getattr(user, 'profile', None)

        errors = {}

        if profile is None:
            errors['profile'] = 'Un profil public est requis avant la publication.'
        else:
            if not profile.title.strip():
                errors['profile.title'] = 'Le titre professionnel est requis.'

        visible_projects = user.projects.exclude(status=Project.Status.ARCHIVED)
        if not visible_projects.exists():
            errors['projects'] = 'Au moins un projet publié ou visible est requis.'

        if errors:
            raise ValidationError(errors)

    def publish(self):
        self.validate()
        self.portfolio.publish()
        return self.portfolio

