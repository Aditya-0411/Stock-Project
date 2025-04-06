from django.db import models
from django.contrib.auth.models import User




class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
class Query(models.Model):
    QUERY_CHOICES = (
        ('Subscription', 'Issue with Subscription'),
        ('Payment', 'Payment Issue'),
        ('Report', 'Report Not Available'),

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query_type = models.CharField(max_length=50, choices=QUERY_CHOICES)
    description = models.TextField()
    assigned_to = models.ForeignKey(Employee, related_name='assigned_queries' ,on_delete=models.SET_NULL, null=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.query_type}"


