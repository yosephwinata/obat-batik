# Generated by Django 3.2.6 on 2022-01-16 11:04

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ingredient', '0001_initial'),
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateField(db_index=True)),
                ('invoice_number', models.CharField(blank=True, db_index=True, max_length=70)),
                ('notes', models.TextField(blank=True, validators=[django.core.validators.MaxLengthValidator(255)])),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=20)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ingredient.ingredient')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.purchase')),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='purchase_ingredients',
            field=models.ManyToManyField(through='purchase.PurchaseIngredient', to='ingredient.Ingredient'),
        ),
        migrations.AddField(
            model_name='purchase',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='purchases', to='supplier.supplier'),
        ),
    ]
