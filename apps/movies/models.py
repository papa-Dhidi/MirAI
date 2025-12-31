from django.db import models
from django.contrib.auth.models import User

class Watchlist(models.Model):
    """
    A model to store movies that a user wants to watch.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    movie_id = models.IntegerField()
    title = models.CharField(max_length=200)
    poster_path = models.CharField(max_length=200, null=True, blank=True)
    release_year = models.IntegerField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensure a user can only have a specific movie in their watchlist once
        unique_together = ('user', 'movie_id')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.title} ({self.user.username}'s Watchlist)"