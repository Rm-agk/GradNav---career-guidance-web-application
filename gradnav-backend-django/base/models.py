from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}, {self.subject}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=1, choices=[('H', 'Higher'), ('O', 'Ordinary')])
    maths_bonus_applicable = models.BooleanField(default=False)

class Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    percentage = models.IntegerField()
    grade = models.CharField(max_length=2, blank=True)
    points = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        self.grade, self.points = self.calculate_grade_points()
        super(Grade, self).save(*args, **kwargs)