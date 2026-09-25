from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('portfolios', '0002_slug_and_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='slug',
            field=models.SlugField(max_length=150, unique=True, verbose_name='Slug public'),
        ),
    ]
