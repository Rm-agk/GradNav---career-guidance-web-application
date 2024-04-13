# quiz/utils.py

# Adjust import as necessary
def generate_chatgpt_prompt(user):
    from account.models import Profile, Background

    profile = Profile.objects.get(user=user)
    
    # Gathering information from the profile
    skills = ", ".join([skill.name for skill in profile.skills.all()])
    subjects = ", ".join([subject.name for subject in profile.subjects.all()])
    hobbies = ", ".join([hobby.name for hobby in profile.hobbies.all()])
    character_traits = ", ".join([trait.name for trait in profile.character_traits.all()])
    wants_needs = ", ".join([want_need.name for want_need in profile.wants_needs.all()])
    
    # Organizing background information
    background_entries = Background.objects.filter(profiles=profile)
    background_str = ""
    for category in Background.CATEGORY_CHOICES:
        category_code, category_name = category
        entries = background_entries.filter(category=category_code)
        if entries:
            entry_str = ", ".join(entry.detail for entry in entries)
            background_str += f"{category_name}: {entry_str}. "
    
    prompt = f"""
Given a student with the following profile:
- Skills: {skills}
- Academic Focus (Subjects): {subjects}
- Hobbies: {hobbies}
- Character Traits: {character_traits}
- Wants and Needs: {wants_needs}
- Background: {background_str}

Could you recommend:
1. Five career paths that align with these skills, subjects, and personal attributes, including estimated salaries for each career in Ireland.
2. Five university courses in Ireland that the student could pursue, information about each course such as CAO points required for admission, and the universities offering these courses.

For each career path and university course recommended, please provide a brief explanation of why they are suited to the student's profile.
"""
    
    return prompt
