from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Quiz, Category, QuizSubmission 
from account.models import Profile
import datetime

class QuizViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.category = Category.objects.create(name='Science')
        cls.quiz = Quiz.objects.create(
            title='General Science',
            description='A quiz on general science topics',
            category=cls.category,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        cls.profile = Profile.objects.create(user=cls.user)
        
        cls.quiz_url = reverse('quiz', kwargs={'quiz_id': cls.quiz.id})
        cls.login_url = reverse('login')

    def setUp(self):
        # Login before each test
        self.client.login(username='testuser', password='12345')

    def test_quiz_access(self):
        # User accesses the quiz page
        response = self.client.get(self.quiz_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz.html')
        self.assertIn('quiz', response.context)
        self.assertEqual(response.context['quiz'].id, self.quiz.id)

    def test_nonexistent_quiz_access_raises_error(self):
    # Expecting an error when trying to access a non-existent quiz
        with self.assertRaises(AttributeError):
            self.client.get(reverse('quiz', kwargs={'quiz_id': 999}))

    def test_quiz_submission_redirect(self):
        # User submits a quiz score
        response = self.client.post(self.quiz_url, {'score': '7'})
        self.assertRedirects(response, self.quiz_url)

    def test_quiz_submission_message_high_score(self):
        # Check for success message on high score
        response = self.client.post(self.quiz_url, {'score': '8'})
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Click below to get more information" in str(message) for message in messages))

    def test_quiz_submission_message_low_score(self):
        # Check for info message on low score
        response = self.client.post(self.quiz_url, {'score': '3'})
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("You are not recommended for the course" in str(message) for message in messages))
