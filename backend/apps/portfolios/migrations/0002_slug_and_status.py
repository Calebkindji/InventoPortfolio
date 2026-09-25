from django.db import migrations, models


def populate_slugs(apps, schema_editor):
    Portfolio = apps.get_model('portfolios', 'Portfolio')
    User = apps.get_model('accounts', 'CustomUser')
    from django.utils.text import slugify

    used = set(Portfolio.objects.exclude(slug__isnull=True).exclude(slug='').values_list('slug', flat=True))
    for portfolio in Portfolio.objects.filter(slug__isnull=True):
        username = User.objects.get(pk=portfolio.user_id).username
        base = slugify(username) or f'portfolio-{portfolio.user_id}'
        candidate = base
        suffix = 2
        while candidate in used:
            candidate = f'{base}-{suffix}'
            suffix += 1
        portfolio.slug = candidate
        portfolio.save(update_fields=['slug'])
        used.add(candidate)


class Migration(migrations.Migration):
    dependencies = [
        ('portfolios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, null=True, unique=True, verbose_name='Slug public'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'Brouillon'), ('PUBLISHED', 'Publié'), ('ARCHIVED', 'Archivé')], default='DRAFT', max_length=20, verbose_name='Statut de publication'),
        ),
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
    ]
