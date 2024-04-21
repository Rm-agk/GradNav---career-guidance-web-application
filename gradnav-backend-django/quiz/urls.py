from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('all_quiz', views.all_quiz_view, name='all_quiz'),
    path('search/<str:category>', views.search_view, name='search'),
    path('<int:quiz_id>', views.quiz_view, name='quiz'),
    path('popular-quizzes/', popular_quizzes, name='popular_quizzes'),
    path('quiz-image/<str:quiz_title>/', generate_quiz_image, name='generate_quiz_image'),
    path('quiz-details/<str:quiz_title>/', views.quiz_details, name='quiz_details'),
    path('recommendations/', views.get_recommendations, name='get_recommendations'),
]