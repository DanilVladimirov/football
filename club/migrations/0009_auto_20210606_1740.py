# Generated by Django 3.2.4 on 2021-06-06 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0008_player_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='type_player',
        ),
        migrations.AddField(
            model_name='player',
            name='role_player',
            field=models.CharField(choices=[('goalkeeper', 'Воротар'), ('defender', 'Захисник'), ('midfielder', 'Півзахисник'), ('attackers', 'Нападаючі')], default='goalkeeper', max_length=20),
        ),
    ]