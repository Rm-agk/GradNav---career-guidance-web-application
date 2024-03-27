from django.urls import path
from . import views
from .views import popular_quizzes

urlpatterns = [
    path('all_quiz', views.all_quiz_view, name='all_quiz'),
    path('search/<str:category>', views.search_view, name='search'),
    path('<int:quiz_id>', views.quiz_view, name='quiz'),
    path('popular-quizzes/', popular_quizzes, name='popular_quizzes'),
]