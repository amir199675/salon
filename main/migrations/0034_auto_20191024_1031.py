# Generated by Django 2.2.2 on 2019-10-24 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_auto_20191024_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(blank=True, choices=[('customer', 'customer'), ('admin', 'admin')], max_length=32, null=True),
        ),
    ]
