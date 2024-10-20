from django.db import models
from django.contrib.auth.models import User

# Create your models here.


status_choices = [
    ('C', 'Complited'),
    ('P', 'Pending'),
    ('I', 'In-Progress'),
]

priority_choices = [
    ('1', '1️⃣'),
    ('2', '2️⃣'),
    ('3', '3️⃣'),
    ('4', '4️⃣'),
    ('5', '5️⃣'),
]

class Todo(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField()
    is_done = models.BooleanField(default=False)
    status = models.CharField(max_length=2, choices=status_choices)
    priority = models.CharField(max_length=2, choices=priority_choices)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.title