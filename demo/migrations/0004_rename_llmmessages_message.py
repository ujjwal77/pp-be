# Generated by Django 4.2.5 on 2023-09-22 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0003_llmmessages'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LLMMessages',
            new_name='Message',
        ),
    ]
