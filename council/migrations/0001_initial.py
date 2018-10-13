# Generated by Django 2.1.2 on 2018-10-13 19:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import universal.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('siteuser', '0002_auto_20181013_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('title', models.CharField(max_length=50)),
                ('number', models.IntegerField()),
            ],
            options={
                'ordering': ('document', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Council',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', universal.fields.AutoSlugField(blank=True, set_once=True, set_using='name')),
                ('location', models.URLField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('date', models.DateField()),
                ('latin_name', models.CharField(max_length=50, unique=True)),
                ('english_name', models.CharField(blank=True, max_length=150)),
                ('position', models.IntegerField()),
                ('slug', universal.fields.AutoSlugField(blank=True, set_once=True, set_using='latin_name')),
                ('location', models.URLField(blank=True)),
                ('council', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='council.Council')),
                ('pontiff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='siteuser.Pontiff')),
            ],
            options={
                'ordering': ['council', 'latin_name'],
            },
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', universal.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', universal.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('number', models.IntegerField()),
                ('text', models.TextField(max_length=600)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='council.Chapter')),
            ],
            options={
                'ordering': ['chapter', 'number'],
            },
        ),
        migrations.AddField(
            model_name='chapter',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='council.Document'),
        ),
    ]
