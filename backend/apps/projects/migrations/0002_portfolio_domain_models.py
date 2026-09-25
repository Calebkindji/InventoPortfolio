from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):
    dependencies = [
        ('profiles', '0001_initial'),
        ('skills', '0002_profile_skill_and_catalog'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Brouillon'), ('IN_PROGRESS', 'En développement'), ('COMPLETED', 'Terminé'), ('ARCHIVED', 'Archivé')], default='DRAFT', max_length=20, verbose_name='Statut du projet'),
        ),
        migrations.AlterField(
            model_name='project',
            name='progress_percentage',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Progression (%)'),
        ),
        migrations.AddField(
            model_name='project',
            name='role',
            field=models.CharField(blank=True, max_length=150, verbose_name='Rôle dans le projet'),
        ),
        migrations.DeleteModel(name='ProjectMedia'),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('storage_key', models.CharField(max_length=500, unique=True)),
                ('url', models.URLField(blank=True, max_length=1000)),
                ('mime_type', models.CharField(max_length=100)),
                ('size', models.PositiveBigIntegerField(default=0)),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('media_type', models.CharField(choices=[('IMAGE', 'Image'), ('VIDEO', 'Vidéo'), ('DOCUMENT', 'Document')], default='IMAGE', max_length=20)),
            ],
            options={'verbose_name': 'Média', 'verbose_name_plural': 'Médias'},
        ),
        migrations.CreateModel(
            name='ProjectMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('order', models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")),
                ('media', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_media', to='projects.media')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media_gallery', to='projects.project')),
            ],
            options={'verbose_name': 'Média de projet', 'verbose_name_plural': 'Médias de projets', 'ordering': ['order', 'created_at']},
        ),
        migrations.CreateModel(
            name='ProjectSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_skills', to='projects.project')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_skills', to='skills.skill')),
            ],
            options={'verbose_name': 'Compétence de projet', 'verbose_name_plural': 'Compétences de projet'},
        ),
        migrations.CreateModel(
            name='ExternalLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('url', models.URLField(max_length=500)),
                ('label', models.CharField(max_length=120)),
                ('type', models.CharField(choices=[('GITHUB', 'GitHub'), ('GITLAB', 'GitLab'), ('DEMO', 'Démonstration'), ('WEBSITE', 'Site web'), ('LINKEDIN', 'LinkedIn'), ('DOCUMENTATION', 'Documentation'), ('VIDEO', 'Vidéo'), ('OTHER', 'Autre')], default='OTHER', max_length=30)),
                ('order', models.PositiveIntegerField(default=0)),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='external_links', to='profiles.userprofile')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='external_links', to='projects.project')),
            ],
            options={'verbose_name': 'Lien externe', 'verbose_name_plural': 'Liens externes', 'ordering': ['order', 'created_at']},
        ),
        migrations.AddConstraint(
            model_name='projectskill',
            constraint=models.UniqueConstraint(fields=('project', 'skill'), name='unique_project_skill'),
        ),
        migrations.AddConstraint(
            model_name='projectmedia',
            constraint=models.UniqueConstraint(fields=('project', 'media'), name='unique_project_media'),
        ),
        migrations.AddConstraint(
            model_name='externallink',
            constraint=models.CheckConstraint(condition=(models.Q(('profile__isnull', False), ('project__isnull', True)) | models.Q(('profile__isnull', True), ('project__isnull', False))), name='external_link_single_owner'),
        ),
    ]
