# Generated by Django 5.1.2 on 2024-11-04 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('referrals', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referralstatsimplified',
            name='promocode',
            field=models.CharField(max_length=10, verbose_name='Промокод'),
        ),
        migrations.AlterField(
            model_name='referralstatsimplified',
            name='username',
            field=models.CharField(max_length=100, verbose_name='Имя пользователя'),
        ),
    ]
