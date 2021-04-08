from django.forms import ModelForm
from SmsBaseApp.models import Contact , Post ,Event , About
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_datepicker_plus import DateTimePickerInput
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _




class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields =['subject', 'name', 'from_email', 'phone', 'message']
class PostForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ['title','slug','author', 'content','status','image']
        
class EventForm(ModelForm):
    
    class Meta:
        model = Event
        fields = ['title','description','Start_event', 'End_event','image']
        widgets = {'Start_event': DateTimePickerInput(),
                    'End_event': DateTimePickerInput()
        }

class AboutForm(ModelForm):
    class Meta:
        model = About
        fields =['data', 'vision', 'mission']
        
        
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    
