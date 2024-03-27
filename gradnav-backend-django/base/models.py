from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from quiz.models import QuizSubmission
import pandas as pd

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

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    submissions_count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quiz_file = models.FileField(upload_to='quiz/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title
    
    def update_submissions_count(self):
        self.submissions_count = QuizSubmission.objects.filter(quiz=self).count()
        self.save()

    # call the function on quiz save
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.quiz_file:
            self.import_quiz_from_excel()

    # function to extract excel file
    def import_quiz_from_excel(self):
        # read teh excel file
        df = pd.read_excel(self.quiz_file.path)

        # iterate over the each row
        for index, row in df.iterrows():
            # extract question text, choices and correct answer from the row
            question_text = row['Question']
            choice1 = row['A']
            choice2 = row['B']
            choice3 = row['C']
            choice4 = row['D']
            correct_answer = row['Answer']

            # create the question object
            question = Question.objects.get_or_create(quiz=self, text=question_text)

            # create choices objects
            choice_1 = Choice.objects.get_or_create(question=question[0], text=choice1, is_correct=correct_answer == 'A')
            choice_2 = Choice.objects.get_or_create(question=question[0], text=choice2, is_correct=correct_answer == 'B')
            choice_3 = Choice.objects.get_or_create(question=question[0], text=choice3, is_correct=correct_answer == 'C')
            choice_4 = Choice.objects.get_or_create(question=question[0], text=choice4, is_correct=correct_answer == 'D')

# Signal to update submissions count after a QuizSubmission is saved
@receiver(post_save, sender=QuizSubmission)
def update_quiz_submissions_count(sender, instance, created, **kwargs):
    instance.quiz.update_submissions_count()