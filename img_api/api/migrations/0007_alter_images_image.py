# Generated by Django 4.1.7 on 2023-02-19 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_rename_image200_images_image_remove_images_image400_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
