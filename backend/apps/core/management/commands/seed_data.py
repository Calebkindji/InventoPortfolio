from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date
from apps.profiles.models import UserProfile
from apps.skills.models import SkillCategory, Skill, ProfileSkill
from apps.experiences.models import Experience
from apps.educations.models import Education
from apps.certifications.models import Certification
from apps.projects.models import Project, ExternalLink, ProjectSkill
from apps.portfolios.models import Portfolio
from apps.portfolios.services import PortfolioPublicationService

User = get_user_model()


class Command(BaseCommand):
    help = "Alimente la base de données avec des données de démonstration réalistes."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Création des données de démonstration..."))

        # 1. Super-utilisateur
        admin_email = "admin@invento.com"
        admin_user, created = User.objects.get_or_create(
            email=admin_email,
            defaults={
                "username": "admin",
                "first_name": "Administrateur",
                "last_name": "INVENTO",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            }
        )
        if created:
            admin_user.set_password("AdminPass123!")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("✔ Super-utilisateur créé : admin@invento.com / AdminPass123!"))
        else:
            self.stdout.write(self.style.SUCCESS("✔ Super-utilisateur existe déjà."))

        # 2. Catégories de compétences
        categories_data = [
            ("Backend", "backend", "Développement côté serveur, bases de données et APIs"),
            ("Frontend", "frontend", "Interfaces utilisateur web et applications clientes"),
            ("DevOps & Cloud", "devops", "Déploiement, CI/CD et infrastructure cloud"),
            ("Mobile", "mobile", "Développement d'applications iOS et Android"),
            ("Data & AI", "data-ai", "Science des données, machine learning et bases NoSQL"),
            ("Design UI/UX", "design", "Conception d'interfaces et expérience utilisateur"),
        ]
        categories = {}
        for name, slug, desc in categories_data:
            cat, _ = SkillCategory.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "description": desc}
            )
            categories[slug] = cat

        # 3. Compétences du catalogue
        skills_data = [
            ("Python", "backend"),
            ("Django REST Framework", "backend"),
            ("FastAPI", "backend"),
            ("PostgreSQL", "backend"),
            ("Redis", "backend"),
            ("React", "frontend"),
            ("TypeScript", "frontend"),
            ("Tailwind CSS", "frontend"),
            ("Next.js", "frontend"),
            ("Docker", "devops"),
            ("Kubernetes", "devops"),
            ("AWS", "devops"),
            ("CI/CD GitHub Actions", "devops"),
            ("Flutter", "mobile"),
            ("Kotlin", "mobile"),
            ("Figma", "design"),
        ]
        skills = {}
        for name, cat_slug in skills_data:
            skill, _ = Skill.objects.get_or_create(
                name=name,
                defaults={"category": categories[cat_slug]}
            )
            skills[name] = skill

        # 4. Utilisateur 1: Jean Dupont (Lead Backend/FullStack)
        jean, created = User.objects.get_or_create(
            email="jean.dupont@invento.com",
            defaults={
                "username": "jeandupont",
                "first_name": "Jean",
                "last_name": "Dupont",
                "role": User.Role.USER,
            }
        )
        if created:
            jean.set_password("StrongPassword123!")
            jean.save()

        jean_profile, _ = UserProfile.objects.get_or_create(user=jean)
        jean_profile.title = "Lead Développeur Full Stack Python / React"
        jean_profile.bio = "Architecte logiciel passionné par le développement d'APIs REST modulaires et d'interfaces réactives."
        jean_profile.location = "Lubumbashi, RDC"
        jean_profile.github_url = "https://github.com/jeandupont"
        jean_profile.linkedin_url = "https://linkedin.com/in/jeandupont"
        jean_profile.professional_email = "pro@jeandupont.dev"
        jean_profile.save()

        # Compétences Jean
        for skill_name, level in [("Python", "EXPERT"), ("Django REST Framework", "EXPERT"), ("React", "ADVANCED"), ("PostgreSQL", "ADVANCED"), ("Docker", "INTERMEDIATE")]:
            ProfileSkill.objects.get_or_create(
                profile=jean_profile,
                skill=skills[skill_name],
                defaults={"level": level}
            )

        # Expériences Jean
        Experience.objects.get_or_create(
            user=jean,
            position="Lead Développeur Backend",
            company="Onyx Innovation",
            defaults={
                "location": "Lubumbashi",
                "start_date": date(2022, 3, 1),
                "is_current": True,
                "description": "Conception et maintenance de microservices Django et architectures cloud.",
                "technologies_used": ["Python", "Django", "PostgreSQL", "Redis", "Docker"]
            }
        )

        # Formations Jean
        Education.objects.get_or_create(
            user=jean,
            degree="Master en Génie Logiciel",
            institution="Université de Lubumbashi",
            defaults={
                "field_of_study": "Informatique & Systèmes",
                "start_date": date(2017, 10, 1),
                "end_date": date(2022, 7, 15),
                "description": "Spécialisation en génie logiciel, bases de données distribuées et sécurité."
            }
        )

        # Certifications Jean
        Certification.objects.get_or_create(
            user=jean,
            name="AWS Certified Solutions Architect",
            issuing_organization="Amazon Web Services",
            defaults={
                "issue_date": date(2023, 5, 10),
                "credential_id": "AWS-ASA-998877",
                "credential_url": "https://aws.amazon.com/verification"
            }
        )

        # Projets Jean
        proj1, _ = Project.objects.get_or_create(
            user=jean,
            title="Aura Player",
            defaults={
                "short_description": "Application multimédia haute performance avec streaming audio/vidéo.",
                "detailed_description": "Aura Player offre une expérience de lecture fluide avec synchronisation cloud et gestion hors ligne.",
                "category": "Web & Mobile",
                "status": Project.Status.COMPLETED,
                "progress_percentage": 100,
                "github_url": "https://github.com/jeandupont/aura-player",
                "demo_url": "https://aura-player.example.com",
                "technologies_used": ["Python", "Django", "React", "PostgreSQL"],
                "is_featured": True,
            }
        )
        ProjectSkill.objects.get_or_create(project=proj1, skill=skills["Python"])
        ProjectSkill.objects.get_or_create(project=proj1, skill=skills["React"])

        proj2, _ = Project.objects.get_or_create(
            user=jean,
            title="Invento Portfolio Engine",
            defaults={
                "short_description": "Moteur backend de publication de portfolios professionnels.",
                "detailed_description": "API REST ultra-rapide construite avec Django REST Framework, JWT, et intégration S3.",
                "category": "Backend",
                "status": Project.Status.IN_PROGRESS,
                "progress_percentage": 85,
                "github_url": "https://github.com/jeandupont/invento-engine",
                "technologies_used": ["Django REST Framework", "PostgreSQL", "Docker", "Redis"],
                "is_featured": True,
            }
        )
        ProjectSkill.objects.get_or_create(project=proj2, skill=skills["Django REST Framework"])

        # Publication Portfolio Jean
        portfolio_jean, _ = Portfolio.objects.get_or_create(user=jean)
        PortfolioPublicationService(portfolio_jean).publish()

        # 5. Utilisateur 2: Sarah Connor (DevOps)
        sarah, created = User.objects.get_or_create(
            email="sarah.connor@invento.com",
            defaults={
                "username": "sarahconnor",
                "first_name": "Sarah",
                "last_name": "Connor",
                "role": User.Role.USER,
            }
        )
        if created:
            sarah.set_password("StrongPassword123!")
            sarah.save()

        sarah_profile, _ = UserProfile.objects.get_or_create(user=sarah)
        sarah_profile.title = "Ingénieure DevOps & Infrastructure Cloud"
        sarah_profile.bio = "Experte en automatisation CI/CD, conteneurisation et orchestration Kubernetes."
        sarah_profile.location = "Kinshasa, RDC"
        sarah_profile.github_url = "https://github.com/sarahconnor"
        sarah_profile.linkedin_url = "https://linkedin.com/in/sarahconnor"
        sarah_profile.save()

        for skill_name, level in [("Docker", "EXPERT"), ("Kubernetes", "EXPERT"), ("AWS", "ADVANCED"), ("CI/CD GitHub Actions", "EXPERT")]:
            ProfileSkill.objects.get_or_create(
                profile=sarah_profile,
                skill=skills[skill_name],
                defaults={"level": level}
            )

        p_sarah, _ = Project.objects.get_or_create(
            user=sarah,
            title="KubeDeploy Automation Pipeline",
            defaults={
                "short_description": "Pipeline d'intégration et déploiement continu zéro-downtime.",
                "detailed_description": "Déploiement automatique de clusters Kubernetes multi-régions.",
                "category": "DevOps",
                "status": Project.Status.COMPLETED,
                "progress_percentage": 100,
                "github_url": "https://github.com/sarahconnor/kubedeploy",
                "technologies_used": ["Docker", "Kubernetes", "AWS", "CI/CD GitHub Actions"],
                "is_featured": True,
            }
        )
        ProjectSkill.objects.get_or_create(project=p_sarah, skill=skills["Kubernetes"])

        portfolio_sarah, _ = Portfolio.objects.get_or_create(user=sarah)
        PortfolioPublicationService(portfolio_sarah).publish()

        self.stdout.write(self.style.SUCCESS("✔ Données de démonstration créées avec succès !"))
        self.stdout.write(self.style.SUCCESS("  - Utilisateurs : admin@invento.com, jean.dupont@invento.com, sarah.connor@invento.com"))
        self.stdout.write(self.style.SUCCESS("  - Portfolios publiés : /u/jeandupont, /u/sarahconnor"))
