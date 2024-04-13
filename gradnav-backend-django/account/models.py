from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Hobby(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class CharacterTrait(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class WantsNeeds(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Background(models.Model):
    CATEGORY_CHOICES = [
        ('family_structure', 'Family Structure'),
        ('socioeconomic_status', 'Socioeconomic Status'),
        ('geographical_background', 'Geographical Background'),
        ('educational_background', 'Educational Background'),
        ('cultural_and_ethnic_identity', 'Cultural And Ethnic Identity'),
        ('religious_background', 'Religious Background'),
        ('health', 'Health'),
        ('language', 'Language'),
        ('work_experience', 'Work Experience'),
        ('mental_health', 'Mental Health'),

        # Add more categories as needed
    ]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    detail = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.get_category_display()}: {self.detail}"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name='User Object')
    bio = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_images', default='user.png', blank=True, null=True, verbose_name='Profile Pic')
    location = models.CharField(max_length=100, blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name='profiles', blank=True)
    subjects = models.ManyToManyField(Subject, related_name='profiles', blank=True)
    hobbies = models.ManyToManyField(Hobby, related_name='profiles', blank=True)
    character_traits = models.ManyToManyField(CharacterTrait, related_name='profiles', blank=True)
    wants_needs = models.ManyToManyField(WantsNeeds, related_name='profiles', blank=True)
    background = models.ManyToManyField(Background, related_name='profiles', blank=True)

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=6, choices=GENDER, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"