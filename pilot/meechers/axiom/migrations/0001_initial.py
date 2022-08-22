# Generated by Django 3.2.14 on 2022-08-18 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.TextField()),
                ('order_id', models.TextField()),
                ('container', models.TextField()),
                ('date_work', models.TextField(default='')),
                ('time_in', models.TextField()),
                ('time_out', models.TextField()),
                ('w1_start', models.TextField()),
                ('w2_start', models.TextField()),
                ('w3_start', models.TextField()),
                ('w4_start', models.TextField()),
                ('w5_start', models.TextField()),
                ('w1_stop', models.TextField()),
                ('w2_stop', models.TextField()),
                ('w3_stop', models.TextField()),
                ('w4_stop', models.TextField()),
                ('w5_stop', models.TextField()),
                ('supervisor', models.TextField()),
                ('product', models.TextField()),
                ('packages', models.TextField()),
                ('sku', models.TextField()),
                ('size', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QrCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('image', models.ImageField(blank=True, upload_to='qrcode')),
            ],
        ),
    ]
