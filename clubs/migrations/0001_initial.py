# Generated by Django 3.0.5 on 2020-04-11 04:41

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizzers', '0004_club_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2020, 4, 11, 4, 41, 34, 948051, tzinfo=utc))),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quizzers.Club')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(default=datetime.datetime(2020, 4, 11, 4, 41, 34, 947324, tzinfo=utc))),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='quizzers.Club')),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('sent_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
