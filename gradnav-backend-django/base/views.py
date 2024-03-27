from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from account.models import Profile
from quiz.models import Quiz, QuizSubmission, Question
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
from .models import Message
from django.db.models import Count, Q
import math
from django.db.models.functions import ExtractYear
from .forms import GradeForm
from .models import Grade
from .models import Quiz


# Create your views here.
@login_required(login_url="login")
def home(request):
    return render(request, 'welcome.html')

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
@login_required(login_url='login')
def dashboard_view(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)


    # Total Number
    total_users = User.objects.all().count()
    total_quizzes = Quiz.objects.all().count()
    total_quiz_submit = QuizSubmission.objects.all().count()
    total_questions = Question.objects.all().count()

    # today_numbers
    today_users = User.objects.filter(date_joined__date=datetime.date.today()).count()
    today_quizzes_objs = Quiz.objects.filter(created_at__date=datetime.date.today())
    today_quizzes = Quiz.objects.filter(created_at__date=datetime.date.today()).count()
    today_quiz_submit = QuizSubmission.objects.filter(submitted_at__date=datetime.date.today()).count()
    today_questions = 0
    for quiz in today_quizzes_objs:
        today_questions += quiz.question_set.count()

    # Gain %
    gain_users = gain_percentage(total_users, today_users)
    gain_quizzes = gain_percentage(total_quizzes, today_quizzes)
    gain_quiz_submit = gain_percentage(total_quiz_submit, today_quiz_submit)
    gain_questions = gain_percentage(total_questions, today_questions)

    # Inbox Messages
    messages = Message.objects.filter(created_at__date=datetime.date.today()).order_by('-created_at')


    context = {"user_profile": user_profile, 
               "total_users": total_users,
               "total_quizzes": total_quizzes,
               "total_quiz_submit": total_quiz_submit,
               "total_questions": total_questions,
               "today_users":today_users,
               "today_quizzes":today_quizzes,
               "today_quiz_submit":today_quiz_submit,
               "today_questions":today_questions,
               "gain_users": gain_users,
               "gain_quizzes": gain_quizzes,
               "gain_quiz_submit": gain_quiz_submit,
               "gain_questions": gain_questions,
               "messages": messages,
               }
    return render(request, "dashboard.html", context)

def gain_percentage(total, today):
    if total > 0 and today > 0:
        gain = math.floor((today *100)/total)
        return gain

def about_view(request):

    if request.user.is_authenticated:
        # request user
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
    else:
        context = {}
    return render(request, "about.html", context)

@login_required(login_url='login')
def contact_view(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject is not None and message is not None:
            form = Message.objects.create(user=request.user, subject=subject, message=message)
            form.save()
            messages.success(request, "We got your message. We will resolve your query soon.")
            return redirect('profile', request.user.username)
        
        else:
            return redirect('contact')
    
    context = {"user_profile": user_profile}
    return render(request, "contact.html", context)

@user_passes_test(is_superuser)
@login_required(login_url='login')
def message_view(request, id):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    message = Message.objects.filter(id=int(id)).first()
    if not message.is_read:
        message.is_read = True
        message.save()

    context = {"user_profile": user_profile, "message": message}
    return render(request, "message.html", context)


def terms_conditions_view(request):

    if request.user.is_authenticated:
        # request user
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile}
    else:
        context = {}
    return render(request, "terms-conditions.html", context)

@login_required(login_url='login')
def downloads_view(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)
    
    context = {"user_profile": user_profile}
    return render(request, "downloads.html", context)

def search_users_view(request):

    query = request.GET.get('q')

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).order_by('date_joined')

    else:
        users = []

    if request.user.is_authenticated:
        # request user
        user_object = User.objects.get(username=request.user)
        user_profile = Profile.objects.get(user=user_object)
        context = {"user_profile": user_profile, "query": query, "users": users}
    else:
        context = {"query": query, "users": users}
    return render(request, "search-users.html", context)

def convert_math_grade_to_points(math_grade):
    math_points = {
        'H1': 125, 'H2': 113, 'H3': 102, 'H4': 91, 'H5': 81, 'H6': 71, 'H7': 33, 'H8': 0,
        'O1': 56, 'O2': 46, 'O3': 37, 'O4': 28, 'O5': 20, 'O6': 13, '07': 0, 'O8': 0,
        'N/A': 0
    }
    return math_points.get(math_grade, 0)

def convert_irish_grade_to_points(irish_grade):
    irish_points = {
        'H1': 125, 'H2': 113, 'H3': 102, 'H4': 91, 'H5': 81, 'H6': 71, 'H7': 33, 'H8': 0,
        'O1': 56, 'O2': 46, 'O3': 37, 'O4': 28, 'O5': 20, 'O6': 13, '07': 0, 'O8': 0,
        'N/A': 0
    }
    return irish_points.get(irish_grade, 0)

def convert_other_subject_grade_to_points(subject_grade):
    subject_points = {
        'H1': 100, 'H2': 88, 'H3': 77, 'H4': 66, 'H5': 56, 'H6': 46, 'H7': 33, 'H8': 0,
        'O1': 56, 'O2': 46, 'O3': 37, 'O4': 28, 'O5': 20, 'O6': 13, '07': 0, 'O8': 0,
        'N/A': 0
    }
    return subject_points.get(subject_grade, 0)

from django.shortcuts import render, redirect
from .forms import GradeForm

def calculate_points(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grades = form.cleaned_data
            points = [
                convert_math_grade_to_points(grades['math_grade']),
                convert_irish_grade_to_points(grades['irish_grade']),
                convert_other_subject_grade_to_points(grades['subject_3_grade']),
                convert_other_subject_grade_to_points(grades['subject_4_grade']),
                convert_other_subject_grade_to_points(grades['subject_5_grade']),
                convert_other_subject_grade_to_points(grades['subject_6_grade']),
                convert_other_subject_grade_to_points(grades['subject_7_grade']),
                convert_other_subject_grade_to_points(grades['subject_8_grade'])
            ]
            
            # Calculate total points from the best 6 results
            total_points = sum(sorted(points, reverse=True)[:6])
            return render(request, 'results.html', {'total_points': total_points})
    else:
        form = GradeForm()
    return render(request, 'calculate.html', {'form': form})


##CHATBOT VIEW
from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View

# Initialize the OpenAI client with your API key
client = openai.api_key = settings.OPENAI_API_KEY

@csrf_exempt  # Use csrf_exempt for demonstration purposes only
@require_http_methods(["POST"])  # Ensure this view only accepts POST requests
def chat_with_gpt(request):
    # Extract user message from the AJAX POST request
    user_message = request.POST.get("message")

    try:
        # Create chat completion with OpenAI
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="gpt-3.5-turbo-0125"  # Adjust the model name as necessary
        )
        # Extract the response
        # Ensure proper access to the message content based on API response structure
        chat_response = chat_completion.choices[0].message.content  # Adjusted access method
    except Exception as e:
        chat_response = f"An error occurred: {str(e)}"

    # Return the chatbot's response in JSON format
    return JsonResponse({"response": chat_response})


def popular_quizzes(request):
    # Retrieve top 5 most popular quizzes based on submissions count
    popular_quizzes = Quiz.objects.order_by('-submissions_count')[:5]
    return render(request, 'popular_quizzes.html', {'popular_quizzes': popular_quizzes})

def quiz_submission(request, quiz_id):
    # Logic to handle quiz submission
    quiz = Quiz.objects.get(id=quiz_id)
    quiz.submissions_count += 1
    quiz.save()
    # Redirect to the quiz page or any other page as needed
    return redirect('quiz', quiz_id)