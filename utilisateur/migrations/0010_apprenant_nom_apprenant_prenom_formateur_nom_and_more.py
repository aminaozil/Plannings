# Generated by Django 5.1.5 on 2025-02-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0009_salle'),
    ]

    operations = [
        migrations.AddField(
            model_name='apprenant',
            name='nom',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='apprenant',
            name='prenom',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='formateur',
            name='nom',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='formateur',
            name='prenom',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
