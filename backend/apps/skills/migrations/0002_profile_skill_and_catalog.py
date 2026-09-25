from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('skills', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(model_name='skill', name='user'),
        migrations.RemoveField(model_name='skill', name='level'),
        migrations.RemoveField(model_name='skill', name='description'),
        migrations.RemoveField(model_name='skill', name='icon'),
        migrations.RemoveField(model_name='skill', name='order'),
        migrations.AlterField(
            model_name='skill',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Nom de la compétence'),
        ),
        migrations.CreateModel(
            name='ProfileSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('level', models.CharField(choices=[('BEGINNER', 'Débutant'), ('INTERMEDIATE', 'Intermédiaire'), ('ADVANCED', 'Avancé'), ('EXPERT', 'Expert')], default='INTERMEDIATE', max_length=20)),
                ('order', models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_skills', to='profiles.userprofile')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_skills', to='skills.skill')),
            ],
            options={
                'verbose_name': 'Compétence du profil',
                'verbose_name_plural': 'Compétences du profil',
                'ordering': ['order', 'skill__name'],
            },
        ),
        migrations.AddConstraint(
            model_name='profileskill',
            constraint=models.UniqueConstraint(fields=('profile', 'skill'), name='unique_profile_skill'),
        ),
    ]
