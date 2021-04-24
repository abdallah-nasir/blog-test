from django import forms
from taggit.forms import TagWidget
from .models import Comments,Post,Category,Author,User
from allauth.account.forms import SignupForm,AddEmailForm
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.auth.forms import UserCreationForm

CATS = (
    ('Art', 'Art'),
    ('Sport', 'Sport and Athletics'),
    ('Science', 'Science Discovery'),        
  )


class PostForm(forms.ModelForm):
    title=forms.CharField(max_length=50)
    category = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Category.objects.all())
    class Meta:
        model = Post
        fields = "__all__"
        exclude=["timestamp","user","votes","approved","views"]
        widgets = {'tags': TagWidget()}
       
        
    def clean(self):
        """Make sure all managers are also members."""
        for cat in self.cleaned_data['category']:
            if cat not in self.cleaned_data['category']:
                self.cleaned_data['category'].append(cat)
        return self.cleaned_data

class AdminForm(forms.ModelForm):
    class Meta:
        model =Post
        fields="__all__"
        exclude = ["timestamp","user"]


    def clean_tags(self):
        for tag in self.cleaned_data["tags"]:
                self.cleaned_data["tags"].append(tag)
                return self.cleaned_data["tags"]
        tn = self.cleaned_data.get('tags', [])
        if len(tn) > 3:
            raise forms.ValidationError('Invalid number of tags', code='invalid')



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["content"]

class MyCustomSignupForm(SignupForm):
    first_name= forms.CharField(max_length=50)
    last_name= forms.CharField(max_length=50)
    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user

class ContactForm(forms.Form):
    subject=forms.CharField(max_length=50)
    message=forms.CharField(widget=forms.Textarea)
   
class ProfileUser(UserCreationForm):
    image=forms.ImageField(required=False)
    class Meta:
        model=User
        fields=["first_name","last_name","email","password1","password2"]


