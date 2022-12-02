from django.shortcuts import render, redirect
from .forms import TopicForm, UserForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from .models import Announcement, Topic, UserProfile

# Create your views here.


def homepage(request):
    latest_announcements_list = Announcement.objects.order_by('-pub_date')[:5]
    context = {'latest_announcements_list': latest_announcements_list}
    return render(request, 'main/home.html', context)

# topics can receive a POST with user topics suscriptions
# topics can receive a GET with all topics and user topics suscriptions
def topics(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            # set the user topics
            user = UserProfile.objects.get(user=request.user)
            user.topics.set(form.cleaned_data['topics'])
            user.save()
            return redirect('main:homepage')
    else:
        # get the user topics and mark them as selected
        user = UserProfile.objects.get(user=request.user)
        form = TopicForm(initial={'topics': user.topics.all()})
    return render(request, 'main/topics.html', {'form': form})

def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('main:homepage')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'main/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })