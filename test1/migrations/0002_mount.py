# Generated by Django 4.2.2 on 2023-10-01 10:55

from django.db import migrations, models
import django.db.models.deletion
import test1.models


class Migration(migrations.Migration):

    dependencies = [
        ('test1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=test1.models.get_upload_path2)),
                ('created_at', models.DateField(auto_now=True)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test1.lab')),
            ],
        ),
    ]