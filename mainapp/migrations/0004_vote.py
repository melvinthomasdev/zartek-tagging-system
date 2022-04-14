# Generated by Django 4.0.4 on 2022-04-14 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0003_tag_alter_postimage_image_posttag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(choices=[(1, 'Like'), (-1, 'Disike')])),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote', to='mainapp.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
