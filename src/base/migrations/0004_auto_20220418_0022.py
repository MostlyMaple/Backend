# Generated by Django 3.1.4 on 2022-04-18 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20220417_2106'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SearchType',
            new_name='DiscountCode',
        ),
        migrations.DeleteModel(
            name='ClothingSize',
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, default='640x360.png', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='image',
            field=models.ImageField(blank=True, default='640x360.png', null=True, upload_to=''),
        ),
    ]
