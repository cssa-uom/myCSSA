# Generated by Django 2.1.3 on 2019-01-23 03:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blogId', models.AutoField(primary_key=True, serialize=False)),
                ('blogTitle', models.CharField(max_length=100)),
                ('blogMainContent', models.TextField(default=None)),
                ('createDate', models.DateTimeField()),
                ('lastModifiedDate', models.DateTimeField(auto_now=True)),
                ('blogReviewed', models.SmallIntegerField(default=0)),
                ('blogOpen', models.BooleanField(default=True)),
                ('blogTopPic', models.ImageField(blank=True, null=True, upload_to='blog/blogpics')),
                ('blogReads', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BlogImage',
            fields=[
                ('imageId', models.AutoField(primary_key=True, serialize=False)),
                ('hashValue', models.CharField(max_length=40)),
                ('imageFileB64', models.ImageField(blank=True, null=True, upload_to='blog/blogpics')),
            ],
        ),
        migrations.CreateModel(
            name='BlogInTag',
            fields=[
                ('blogTagId', models.AutoField(primary_key=True, serialize=False)),
                ('blogId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogAPI.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='BlogOldContent',
            fields=[
                ('blogOldContentId', models.AutoField(primary_key=True, serialize=False)),
                ('blogOldTitle', models.CharField(max_length=100)),
                ('blogOldContent', models.TextField()),
                ('writtenDate', models.DateTimeField(default=None)),
                ('blogId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogAPI.Blog')),
            ],
        ),
        migrations.CreateModel(
            name='BlogReviewed',
            fields=[
                ('reviewedId', models.AutoField(primary_key=True, serialize=False)),
                ('blogId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogAPI.Blog')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlogTag',
            fields=[
                ('tagId', models.AutoField(primary_key=True, serialize=False)),
                ('tagName', models.CharField(max_length=18)),
                ('tagCreateTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BlogWrittenBy',
            fields=[
                ('blogCreatedId', models.AutoField(primary_key=True, serialize=False)),
                ('blogId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogAPI.Blog')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='blogintag',
            name='tagId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogAPI.BlogTag'),
        ),
    ]
