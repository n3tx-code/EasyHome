# Generated by Django 4.1.5 on 2023-02-17 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom')),
                ('hashed_name', models.CharField(max_length=255, verbose_name='Nom chiffré')),
            ],
            options={
                'verbose_name': 'Expense record',
                'verbose_name_plural': 'Expense ecords',
            },
        ),
    ]
