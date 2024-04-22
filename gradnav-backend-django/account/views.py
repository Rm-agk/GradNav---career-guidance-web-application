from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from quiz.models import *
from .forms import *
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Profile, Skill, Subject, Hobby, CharacterTrait, WantsNeeds, Background

def register(request):
    if request.user.is_authenticated:
        return redirect('profile', username=request.user.username)

    step = request.session.get('register_step', 1)
    template_name = f'register_step{step}.html'

    if request.method == 'POST':
        if step == 1:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user_data = form.cleaned_data.copy()
                user_data.pop('password2', None)  # Remove 'password2' from the data
                request.session['register_form_data'] = user_data
                request.session['register_step'] = 2
                request.session.modified = True
                return redirect('register')
        elif step == 2:
            form = SubjectsForm(request.POST)
            if form.is_valid():
                subjects_ids = list(form.cleaned_data['subjects'].values_list('id', flat=True))
                request.session['subjects_form_data'] = subjects_ids
                request.session['register_step'] = 3
                request.session.modified = True
                return redirect('register')
        elif step == 3:
            form = SkillsForm(request.POST)
            if form.is_valid():
                skills_ids = list(form.cleaned_data['skills'].values_list('id', flat=True))
                request.session['skills_form_data'] = skills_ids
                request.session['register_step'] = 4
                request.session.modified = True
                return redirect('register')
        elif step == 4:
            form = HobbiesForm(request.POST)
            if form.is_valid():
                hobbies_ids = list(form.cleaned_data['hobbies'].values_list('id', flat=True))
                request.session['hobbies_form_data'] = hobbies_ids
                request.session['register_step'] = 5
                request.session.modified = True
                return redirect('register')
        elif step == 5:
            form = CharacterTraitsForm(request.POST)
            if form.is_valid():
                character_traits_ids = list(form.cleaned_data['character_traits'].values_list('id', flat=True))
                request.session['character_traits_form_data'] = character_traits_ids
                request.session['register_step'] = 6
                request.session.modified = True
                return redirect('register')
        elif step == 6:
            form = WantsNeedsForm(request.POST)
            if form.is_valid():
                wants_needs_ids = list(form.cleaned_data['wants_needs'].values_list('id', flat=True))
                request.session['wants_needs_form_data'] = wants_needs_ids
                request.session['register_step'] = 7
                request.session.modified = True
                return redirect('register')
        elif step == 7:
            form = BackgroundForm(request.POST)
            if form.is_valid():
                background_ids = list(form.cleaned_data['background'].values_list('id', flat=True))
                request.session['background_form_data'] = background_ids
                # All data collected, create user and profile
                with transaction.atomic():
                    user_data = request.session.get('register_form_data')
                    user = User.objects.create_user(username=user_data['username'], email=user_data['email'], password=user_data['password'])
                    profile = Profile.objects.create(user=user)
                    profile.subjects.set(Subject.objects.filter(id__in=request.session.get('subjects_form_data', [])))
                    profile.skills.set(Skill.objects.filter(id__in=request.session.get('skills_form_data', [])))
                    profile.hobbies.set(Hobby.objects.filter(id__in=request.session.get('hobbies_form_data', [])))
                    profile.character_traits.set(CharacterTrait.objects.filter(id__in=request.session.get('character_traits_form_data', [])))
                    profile.wants_needs.set(WantsNeeds.objects.filter(id__in=request.session.get('wants_needs_form_data', [])))
                    profile.background.set(Background.objects.filter(id__in=request.session.get('background_form_data', [])))
                    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    # Clear the session data
                    del request.session['register_form_data']
                    del request.session['subjects_form_data']
                    del request.session['skills_form_data']
                    del request.session['hobbies_form_data']
                    del request.session['character_traits_form_data']
                    del request.session['wants_needs_form_data']
                    del request.session['background_form_data']
                    del request.session['register_step']
                    return redirect('get_recommendations')

    else:
        # Determine which form to display based on the current step
        form = None
        template_name = f'register_step{step}.html'  # Dynamically set template based on step

        if step == 1:
            form = RegisterForm()
        elif step == 2:
            form = SubjectsForm()
        elif step == 3:
            form = SkillsForm()
        elif step == 4:
            form = HobbiesForm()
        elif step == 5:
            form = CharacterTraitsForm()
        elif step == 6:
            form = WantsNeedsForm()
        elif step == 7:
            form = BackgroundForm()

    context = {'form': form}
    return render(request, template_name, context)



@login_required(login_url='login')
def profile(request, username):
    user_profile = get_object_or_404(User, username=username).profile
    skills = user_profile.skills.all()
    subjects = user_profile.subjects.all()
    hobbies = user_profile.hobbies.all()
    character_traits = user_profile.character_traits.all()
    wants_needs = user_profile.wants_needs.all()
    background = user_profile.background.all()

    context = {
        "user_profile": user_profile,
        "skills": skills,
        "subjects": subjects,
        "hobbies": hobbies,
        "character_traits": character_traits,
        "wants_needs": wants_needs,
        "background": background,
    }
    return render(request, "profile.html", context)

@login_required(login_url='login')
def editProfile(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        # Image upload handling
        if request.FILES.get('profile_img') is not None:
            user_profile.profile_img = request.FILES.get('profile_img')
            user_profile.save()

        # Email update handling
        email = request.POST.get('email')
        if email and email != user_object.email:
            if User.objects.filter(email=email).exclude(id=user_object.id).exists():
                messages.error(request, "Email already in use. Please choose another.")
                return redirect('edit_profile')
            else:
                user_object.email = email
                user_object.save()

        # Username update handling
        username = request.POST.get('username')
        if username and username != user_object.username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken. Please choose another.")
                return redirect('edit_profile')
            else:
                user_object.username = username
                user_object.save()

        # First name and last name update handling
        user_object.first_name = request.POST.get('firstname')
        user_object.last_name = request.POST.get('lastname')
        user_object.save()

        # Profile updates for location, bio, and gender
        user_profile.location = request.POST.get('location')
        user_profile.gender = request.POST.get('gender')
        user_profile.bio = request.POST.get('bio')
        user_profile.save()

        # Handling `ManyToManyField` updates
        skills_form = SkillsForm(request.POST, instance=user_profile)
        subjects_form = SubjectsForm(request.POST, instance=user_profile)
        hobbies_form = HobbiesForm(request.POST, instance=user_profile)
        character_traits_form = CharacterTraitsForm(request.POST, instance=user_profile)
        wants_needs_form = WantsNeedsForm(request.POST, instance=user_profile)
        background_form = BackgroundForm(request.POST, instance=user_profile)

        forms = [skills_form, subjects_form, hobbies_form, character_traits_form, wants_needs_form, background_form]
        if all(form.is_valid() for form in forms):
            for form in forms:
                form.save()
        else:
            messages.error(request, "Please correct the errors in the form.")
            return redirect('edit_profile')

        messages.success(request, "Profile updated successfully.")
        return redirect('profile', username=user_object.username)

    else:
        # Initialize forms with current data for GET request
        skills_form = SkillsForm(instance=user_profile)
        subjects_form = SubjectsForm(instance=user_profile)
        hobbies_form = HobbiesForm(instance=user_profile)
        character_traits_form = CharacterTraitsForm(instance=user_profile)
        wants_needs_form = WantsNeedsForm(instance=user_profile)
        background_form = BackgroundForm(instance=user_profile)

        context = {
            "user_profile": user_profile,
            "skills_form": skills_form,
            "subjects_form": subjects_form,
            "hobbies_form": hobbies_form,
            "character_traits_form": character_traits_form,
            "wants_needs_form": wants_needs_form,
            "background_form": background_form
        }
        return render(request, 'profile-edit.html', context)


@login_required(login_url='login')
def deleteProfile(request):

    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        user_profile.delete()
        user_object.delete()
        return redirect('logout')



    context = {"user_profile": user_profile}
    return render(request, 'confirm.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('profile', username)
        else:
            messages.info(request, 'Credentials Invalid!')
            return redirect('login')

    return render(request, "login.html")

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')