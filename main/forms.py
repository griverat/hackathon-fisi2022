from django import forms
from django.contrib.auth.models import User

from .models import Announcement, Topic, UserProfile


# Multiple choice froms showing the topics the user can subscribe to
class TopicForm(forms.Form):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = UserProfile
        fields = ("topics",)


# Form that allows users to change their name and email
class UserForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"readonly": "readonly"}), required=False
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


# Form that allows users to change their profile information
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("topics",)
