from django.db import models
from django.contrib.auth.models import User

# Snippet below regarding category choices inspired by:
# https://bit.ly/3HHDAyC
CATEGORY_CHOICES = (
    ("Breakfast", "Breakfast"),
    ("Appetizer", "Appetizer"),
    ("Entrée", "Entrée"),
    ("Dessert", "Dessert"),
    ("Snacks", "Snacks"),
    )


class Recipe(models.Model):
    """
    Recipe model class
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default=""
        )
    ingredient = models.TextField(blank=True)
    instruction = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_recipe_zpx4vg', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'
