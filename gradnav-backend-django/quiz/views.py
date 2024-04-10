from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Profile
from .models import Quiz, Category
from django.db.models import Q
from quiz.models import QuizSubmission
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
def all_quiz_view(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    quizzes = Quiz.objects.order_by('-created_at')
    categories = Category.objects.all()

    context = {"user_profile": user_profile, "quizzes": quizzes, "categories": categories}
    return render(request, 'all-quiz.html', context)

@login_required(login_url='login')
def search_view(request, category):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    # search by search bar
    if request.GET.get('q') != None:
        q = request.GET.get('q')
        query = Q(title__icontains=q) | Q(description__icontains=q)
        quizzes = Quiz.objects.filter(query).order_by('-created_at')
    
    # search by category
    elif category != " ":
        quizzes = Quiz.objects.filter(category__name=category).order_by('-created_at')
    
    else:
        quizzes = Quiz.objects.order_by('-created_at')


    categories = Category.objects.all()

    context = {"user_profile": user_profile, "quizzes": quizzes, "categories": categories}
    return render(request, 'all-quiz.html', context)

@login_required(login_url='login')
def quiz_view(request, quiz_id):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    quiz = Quiz.objects.filter(id=quiz_id).first()

    total_questions = quiz.question_set.all().count()

    if request.method == "POST":
        
        # Get the score
        score = int(request.POST.get('score', 0))

        # Check if the user has already submiited the quiz
        if QuizSubmission.objects.filter(user=request.user, quiz=quiz).exists():
            messages.success(request, f"This time you got {score} out of {total_questions}")
            return redirect('quiz', quiz_id)
        
        # save the new quiz submission
        submission = QuizSubmission(user=request.user, quiz=quiz, score=score)
        submission.save()

        # show the result in message
        messages.success(request,f"Quiz Submitted Successfully. You got {score} out of {total_questions}")
        return redirect('quiz', quiz_id)

    if quiz != None:
        context = {"user_profile": user_profile, "quiz": quiz}
    else:
        return redirect('all_quiz')
    return render(request, 'quiz.html', context)

from django.shortcuts import render
from .models import Quiz

def popular_quizzes(request):
    popular_quizzes = Quiz.objects.order_by('-submissions_count')[:6]
    return render(request, 'popular_quizzes.html', {'popular_quizzes': popular_quizzes})


import requests

def generate_quiz_image(request, quiz_title):
    api_key = 'AIzaSyCzRFLYY6wTAHaah0C6hIzvsLJEqMSsKtk'
    cx = 'c2755331ec3c04fc9'

    # Make API request to Google Custom Search API
    url = f'https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&searchType=image&q={quiz_title}'
    response = requests.get(url)
    data = response.json()

    # Extract image URL from API response
    if 'items' in data:
        image_url = data['items'][0]['link']  # Get the first image URL
    else:
        # If no image found, use a default image or handle the case as needed
        image_url = 'https://example.com/default_image.png'

    # Return a redirect response to the image URL
    return redirect(image_url)

from openai import ChatCompletion

def quiz_details(request, quiz_title):
    # Fetch additional information using the quiz title
    additional_info = get_additional_info(quiz_title)

    # Pass the retrieved information to the template
    context = {
        'quiz_title': quiz_title,
        'additional_info': additional_info,
    }
    return render(request, 'quiz_details.html', context)

import openai
import re
from django.conf import settings

def get_additional_info(quiz_title):
    openai.api_key = settings.OPENAI_API_KEY

    prompt = f"""Given the quiz title '{quiz_title}', provide the following information:
1. Related job opportunities and their descriptions and personality types that suit the role.
2. Bachelor's degree courses available in Ireland related to the quiz topic and what colleges they can be studied in with points to match.
3. Salary insights for jobs related to the quiz topic.
4. Nearby accommodation options for students based on the courses recommended.
5. Any other relevant information.
"""

    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1000,
            n=1,
            stop=None
        )
        text_response = response.choices[0].text.strip()

        # Split the response into sections
        sections = re.split(r'\n\d\.\s', text_response)
        if sections[0] == '':
            sections.pop(0)  # Remove the first element if it's empty or does not contain useful info

        additional_info = {'sections': sections}

    except Exception as e:
        additional_info = {
            'sections': [f"An error occurred: {str(e)}"]  # Wrap the error message in a list for consistency
        }

    return additional_info
