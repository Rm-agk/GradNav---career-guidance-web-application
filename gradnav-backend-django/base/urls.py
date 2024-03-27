from django.urls import path
from . import views
from .views import calculate_points


urlpatterns = [
    path('', views.home, name='home'),
    path('leaderboard', views.leaderboard_view, name='leaderboard'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('message/<int:id>', views.message_view, name='message'),
    path('about', views.about_view, name='about'),
    path('contact', views.contact_view, name='contact'),
    path('terms_and_conditions', views.terms_conditions_view, name='terms_conditions'),
    path('downloads', views.downloads_view, name='downloads'),
    path('search/users', views.search_users_view, name='search_users'),
    path('calculate', calculate_points, name='calculate'),
    path('chat/', views.chat_with_gpt, name='chat_with_gpt'),
    path('popular-quizzes/', views.popular_quizzes, name='popular_quizzes'),
    path('quiz-submission/<int:quiz_id>/', views.quiz_submission, name='quiz_submission'),
]