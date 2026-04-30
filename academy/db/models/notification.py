from django.db import models


class Notification(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    TYPE_CHOICES = (
        ('ROSTER_PUBLISHED', 'Roster Published'),
        ('MAINTENANCE', 'Maintenance'),
        ('GENERAL', 'General'),
    )

    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')

    class Meta:
        db_table = "notification"


class UserNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey('db.User', on_delete=models.CASCADE)

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "user_notification"
        unique_together = ('notification', 'user')
