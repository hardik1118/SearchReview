# Generated by Django 3.2.4 on 2022-07-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prodId', models.CharField(max_length=20)),
                ('userId', models.CharField(max_length=20)),
                ('profName', models.CharField(max_length=50)),
                ('help', models.DecimalField(decimal_places=2, max_digits=3)),
                ('score', models.DecimalField(decimal_places=2, max_digits=3)),
                ('time', models.CharField(max_length=20)),
                ('summary', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=2000)),
            ],
        ),
    ]
