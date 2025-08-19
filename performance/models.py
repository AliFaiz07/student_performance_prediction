# performance/models.py

from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)

    attendance = models.FloatField()
    assignment_score = models.FloatField()
    test_score = models.FloatField()
    teacher_feedback = models.TextField()

    prediction_score = models.FloatField(null=True, blank=True)
    result = models.CharField(max_length=10, null=True, blank=True)
    pin = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name
