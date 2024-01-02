# Generated by Django 5.0 on 2024-01-02 01:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_alter_uploadedvideo_subtitles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedvideo',
            name='subtitles',
        ),
        migrations.CreateModel(
            name='Subs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtitles', models.FileField(blank=True, upload_to='')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upload.uploadedvideo')),
            ],
        ),
    ]
