from django.db import models

# Create your models here.

class Account(models.Model):

    STATUSES = (
        ('pending', 'Pending'),
        ('queued', 'Queued'),
        ('done', 'Done'),
        ('failed', 'Failed'),
        ('ignored', 'Ignored')
    )

    username = models.CharField(max_length=100, unique=True)
    account_id = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUSES, default='pending')
    bio = models.CharField(max_length=5000, default='', blank=True, null=False)
    follower_count = models.IntegerField(default=0)
    followed_by_count = models.IntegerField(default=0)
    avatar_url = models.CharField(max_length=500, blank=True, null=True)

    def serialize(self):
        return {
            "username":self.username,
            "account_id":self.account_id,
            "bio":self.bio,
            "follower_count":self.follower_count,
            "followed_by_count":self.followed_by_count,
            "avatar_url":self.avatar_url
        }