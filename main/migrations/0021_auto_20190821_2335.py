# Generated by Django 2.2.2 on 2019-08-21 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_training_class_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gym',
            name='famous',
            field=models.CharField(blank=True, choices=[('Number_one', 'number_one'), ('Number_two', 'number_two'), ('None', 'none')], default='None', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='gym',
            name='latitude',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gym',
            name='longitude',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gym',
            name='mobile',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='gym',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='gym',
            name='score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='gym',
            name='sex',
            field=models.CharField(blank=True, choices=[('مرد', 'man'), ('زن', 'woman')], default='مرد', max_length=32, null=True),
        ),
    ]