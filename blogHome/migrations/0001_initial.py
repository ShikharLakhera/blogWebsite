# Generated by Django 4.2.7 on 2025-02-16 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=25)),
                ('timeStamp', models.DateTimeField(blank=True)),
                ('slug', models.CharField(max_length=200)),
            ],
        ),
    ]
