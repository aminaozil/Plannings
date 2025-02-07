# Generated by Django 5.1.5 on 2025-02-01 22:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0006_filiere_matiere_alter_matiere_nom_matiere'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_classe', models.CharField(max_length=200)),
                ('filiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.filiere')),
            ],
        ),
    ]
