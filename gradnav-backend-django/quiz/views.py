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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import Profile
from .models import Quiz, QuizSubmission

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quiz, QuizSubmission

@login_required(login_url='login')
def quiz_view(request, quiz_id):
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)
    quiz = Quiz.objects.filter(id=quiz_id).first()
    total_questions = quiz.question_set.all().count()

    # This check ensures that the quiz exists before proceeding
    if not quiz:
        messages.error(request, "The requested quiz does not exist.")
        return redirect('all_quiz')

    if request.method == "POST":
        score = int(request.POST.get('score', 0))
        
        # Check if the user has already submitted this quiz and update the score
        submission, created = QuizSubmission.objects.update_or_create(
            user=request.user, 
            quiz=quiz, 
            defaults={'score': score}
        )
        
        # Provide feedback to the user based on the score
        if score >= 5:
            # Set the session variable to true to indicate that the additional information should be displayed
            request.session['display_additional_info'] = True
            messages.success(request, f"You scored {score} out of {total_questions}. Click below to get more information.")
        else:
            # If the score is less than 5, inform the user they are not recommended for the course
            messages.info(request, f"You scored {score} out of {total_questions}. You are not recommended for the course.")
        
        # Redirect to the same quiz page to display the messages
        return redirect('quiz', quiz_id=quiz_id)

    # If it's a GET request, display the quiz
    # The display_additional_info is popped from the session to check if the button should be displayed
    context = {
        "user_profile": user_profile,
        "quiz": quiz,
        "total_questions": total_questions,
        # The pop method will remove the display_additional_info from the session after accessing its value
        "display_additional_info": request.session.pop('display_additional_info', False)
    }
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

    cat = [
        "Job opportunities",
        "Bachelor's degree courses",
        "Salary insights",
        "Nearby accommodation",
        "Other relevant information"
    ]

    # Pass the retrieved information to the template
    context = {
        'quiz_title': quiz_title,
        'additional_info': additional_info,
        'cat':cat
    }
    return render(request, 'quiz_details.html', context)

import openai
import re
from django.conf import settings

def get_additional_info(quiz_title):
    openai.api_key = settings.OPENAI_API_KEY

    prompt = f"""Given the quiz title '{quiz_title}', provide detailed information on the following information:
1. Related job opportunities and their descriptions and personality types that suit the role.
2. Bachelor's degree courses available in Ireland related to the quiz topic and what colleges they can be studied in with points to match.
3. Salary insights for per job opportunity related to the quiz topic for an entry level position and with career progression.
4. Nearby accommodation options (by name) for each college mentioned.
5. Any other relevant information e.g. if further education after level 8 required, there is demand for role etc.
"""

    try:
        client = openai.OpenAI()  # Initialize the OpenAI client
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=1000
        )

        # Assuming the response object has a method to convert to dictionary if it's not directly subscriptable
        if hasattr(response, 'to_dict'):
            response_data = response.to_dict()
        else:
            response_data = response

        text_response = response_data['choices'][0]['message']['content'].strip()

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





from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .utils import generate_chatgpt_prompt
from django.contrib.auth.decorators import login_required

# Ensure OpenAI client is initialized (as shown above)
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


@login_required
@csrf_exempt  # Consider security implications in production
def get_recommendations(request):
    # This endpoint might be adapted to POST if fetching dynamic user data
    if request.method == "GET":
        # Generate the comprehensive prompt from the user's profile and quiz responses
        prompt = generate_chatgpt_prompt(request.user)

        try:
            # Create chat completion with OpenAI
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Adjust the model name as necessary
                messages=[
                    {"role": "system", "content": "You are a knowledgeable assistant asked to provide course and career recommendations."},
                    {"role": "user", "content": prompt}
                ]
            )
            # Extract the recommendations from the response
            recommendations = chat_completion.choices[0].message.content  # Ensure this matches the actual response structure
        except Exception as e:
            recommendations = f"An error occurred: {str(e)}"

        # Assuming you want to return the recommendations to be displayed on a webpage
        return render(request, 'recommendations.html', {'recommendations': recommendations})
    else:
        # Handle unexpected method
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
import openai

@login_required
def display_additional_info(request, quiz_title):
    # Ensure the user has scored enough to access this view.
    # If not, redirect them and show a warning message.
    if not request.session.get('display_additional_info', False):
        messages.warning(request, "")
        # Redirect to the detailed quiz view.
        return redirect('quiz_details', quiz_title=quiz_title)

    # Clear the session variable after checking it.
    del request.session['display_additional_info']

    # OpenAI API call logic
    openai.api_key = settings.OPENAI_API_KEY
    prompt = f"""
Given the quiz title '{quiz_title}', provide the following information:
1. Related job opportunities and their descriptions and personality types that suit the role.
2. Bachelor's degree courses available in Ireland related to the quiz topic and what colleges they can be studied in with points to match.
3. Salary insights for jobs related to the quiz topic.
4. Nearby accommodation options for students based on the courses recommended.
5. Any other relevant information.
"""
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1000
        )
        text_response = response.choices[0].message['content'].strip()
    except Exception as e:
        messages.error(request, f"An error occurred while retrieving additional information: {e}")
        return redirect('quiz_details', quiz_title=quiz_title)

    # Return the additional information as an HttpResponse
    return HttpResponse(text_response, content_type="text/plain")