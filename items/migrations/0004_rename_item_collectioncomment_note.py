# Generated by Django 5.2 on 2025-04-29 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_rename_collectioncomments_collectioncomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collectioncomment',
            old_name='item',
            new_name='note',
        ),
    ]
