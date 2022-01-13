# Generated by Django 3.2.6 on 2022-01-09 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0001_initial'),
        ('purchase', '0002_alter_purchase_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=20)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='ingredient.ingredient')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.purchase')),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='purchase_ingredients',
            field=models.ManyToManyField(through='purchase.PurchaseIngredient', to='ingredient.Ingredient'),
        ),
    ]
