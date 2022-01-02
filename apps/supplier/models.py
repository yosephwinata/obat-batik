from django.db import models
from django.utils.text import slugify

# Create your models here.

class Supplier(models.Model):
    name = models.CharField(unique=True, max_length=70, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Supplier, self).save(*args, **kwargs)