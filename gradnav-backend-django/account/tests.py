from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Skill, Subject, Hobby, CharacterTrait, WantsNeeds, Background

class RegisterViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        Profile.objects.create(user=self.user)
        self.skills = [Skill.objects.create(name="Creativity")]
        self.subjects = [Subject.objects.create(name="Music")]
        self.hobbies = [Hobby.objects.create(name="Dancing")]
        self.character_traits = [CharacterTrait.objects.create(name="Driven")]
        self.wants_needs = [WantsNeeds.objects.create(name="Career Stability")]
        self.backgrounds = [Background.objects.create(category='family_structure', detail='Big Family')]
        self.register_url = reverse('register')
        self.profile_url = reverse('profile', kwargs={'username': self.user.username})
        self.get_recommendations_url = reverse('get_recommendations')

    def test_authenticated_redirect(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.register_url)
        self.assertRedirects(response, self.profile_url)

    def test_register_step_one_valid(self):
        self.client.session['register_step'] = 1  # Set the step explicitly
        self.client.session.save()  # Make sure session is saved before the request
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepassword123',
            'password2': 'securepassword123',
        }
        response = self.client.post(self.register_url, form_data)
        self.client.session.save()  # Save session after the post
        self.assertEqual(self.client.session.get('register_step'), 2)
