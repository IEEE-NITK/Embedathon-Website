# Generated by Django 4.0.2 on 2022-02-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('embedathon', '0002_alter_team_member_alter_team_teamname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='passcode',
            field=models.CharField(max_length=6, unique=True, verbose_name='Team Passcode'),
        ),
    ]