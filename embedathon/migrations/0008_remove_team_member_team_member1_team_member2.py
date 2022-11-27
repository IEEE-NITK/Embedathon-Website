# Generated by Django 4.0 on 2022-11-26 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('embedathon', '0007_alter_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='member',
        ),
        migrations.AddField(
            model_name='team',
            name='member1',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_member_1', to='embedathon.user'),
        ),
        migrations.AddField(
            model_name='team',
            name='member2',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_member_2', to='embedathon.user'),
        ),
    ]
