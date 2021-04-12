from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=256)

class Institution(models.Model):
    FOUNDATION_TYPES = [
        (0, 'Fundacja'),
        (1, 'Organizacja pozarządowa'),
        (2, 'Zbiórka lokalna')
    ]
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.IntegerField(choices=FOUNDATION_TYPES, default=0)
    categories = models.ManyToManyField(Category)
