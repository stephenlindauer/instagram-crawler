from django.db import models

# Create your models here.

class Account(models.Model):

    STATUSES = (
        ('pending', 'Pending'),
        ('queued', 'Queued'),
        ('done', 'Done'),
        ('failed', 'Failed')
    )

    username = models.CharField(max_length=100)
    account_id = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUSES, default='pending')
    bio = models.CharField(max_length=5000, default='', blank=True, null=False)
    follower_count = models.IntegerField(default=0)
    followed_by_count = models.IntegerField(default=0)