from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe


class Save(models.Model):
    """
    Save model class
    'unique_together' makes sure a user can't save the same post twice
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, related_name='saves', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'recipe']

    def __str__(self):
        return f'{self.owner} {self.recipe}'
