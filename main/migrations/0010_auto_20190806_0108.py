# Generated by Django 2.2.2 on 2019-08-06 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_training_class_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='gym_id',
            field=models.ManyToManyField(blank=True, null=True, related_name='group', to='main.Gym'),
        ),
        migrations.AlterField(
            model_name='gym',
            name='category_id',
            field=models.ManyToManyField(blank=True, null=True, related_name='categories', to='main.Category'),
        ),
    ]