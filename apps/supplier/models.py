from django.db import models

# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=70)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name