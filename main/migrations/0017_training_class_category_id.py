# Generated by Django 2.2.2 on 2019-08-11 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20190810_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='training_class',
            name='category_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Category'),
        ),
    ]
