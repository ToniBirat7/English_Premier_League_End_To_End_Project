from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)
    stadium = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    website = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Teams'

    def __str__(self):
        return self.name

    @property
    def full_name(self):
        return f"{self.name} ({self.short_name})" 