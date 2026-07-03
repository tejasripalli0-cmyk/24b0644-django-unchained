from django.conf import settings
from django.db import models


class Bounty(models.Model):
    """
    Represents a bounty posted on the Bounty Board.
    """

    class Status(models.TextChoices):
        WANTED = 'wanted', 'Wanted'
        CAPTURED = 'captured', 'Captured'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bounties',
    )
    target_name = models.CharField(max_length=255)
    reward = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.WANTED,
    )
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Bounty'
        verbose_name_plural = 'Bounties'

    def __str__(self):
        return f'{self.target_name} ({self.status}) - {self.reward}'

