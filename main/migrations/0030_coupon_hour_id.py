# Generated by Django 2.2.2 on 2019-10-17 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_merge_20190828_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='hour_id',
            field=models.ManyToManyField(blank=True, null=True, related_name='hour', to='main.Hour'),
        ),
    ]
