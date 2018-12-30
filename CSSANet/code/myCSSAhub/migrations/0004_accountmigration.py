# Generated by Django 2.1.3 on 2018-12-29 06:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('myCSSAhub', '0003_auto_20181228_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountMigration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time', models.DateField(auto_now_add=True)),
                ('studentId', models.CharField(max_length=10, verbose_name='学生证号')),
                ('membershipId', models.CharField(max_length=10, verbose_name='会员卡号')),
            ],
        ),
    ]
