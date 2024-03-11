from pyexpat import model
from django.db.models import fields
from django.db.models.base import Model
from django.forms.models import ModelForm
from Rare_app.models import Artist_detail, Blog, ContactUs, CustomerContact, Post,FAQ
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserCreationForm,AuthenticationForm
from django import forms
from django.contrib.auth.models import User

#-------------------------------------------Artist Form-----------------------------------------------------

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist_detail
        fields = ['adhar','contact','address']
        widgets={
        'adhar':forms.FileInput(attrs={'class':'form-control','style':'padding-top: 1em; padding-left: 1.5em;'}),
        'contact':forms.NumberInput(attrs={'class':'form-control','placeholder':'CONTACT'}),
        'address':forms.TextInput(attrs={'class':'form-control','placeholder':'ADDRESS'})
        }

#-------------------------------------------Registration Form-----------------------------------------------------

class RegUser(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Re-renter password'}),label='Confirm Password')
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        widgets = {'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
        'email':forms.TextInput(attrs={'class':'form-control','placeholder':'email'}),
        'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First name'}),
        'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last name'})
        }

        labels = {'username':'Username','first_name':'First Name','last_name':'Last Name','email':'Email'}

#----------------------------------------------Edit Profile form--------------------------------------------------

class EditProfile(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        widgets = {
        'email':forms.TextInput(attrs={'class':'form-control','placeholder':'email'}),
        'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First name'}),
        'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last name'})
        }


#-------------------------------------------Login Form--------------------------------------------------------

class LoginUser(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),label='Password')
    class Meta:
        model = User
        fields = ['username','password']



#-------------------------------------------New Product Form-----------------------------------------------------
st = ((True,'Is it available ?'),(True,True),(False,False))
class NewPost(forms.ModelForm):
    
    class Meta:
        model=Post
        fields = '__all__'
        exclude = ['posted_by','posted_at','like']
        widgets={
       
        'title':forms.TextInput(attrs={'class':'form-control','placeholder':'title'}),
        'category':forms.Select(attrs={'class':'form-control','placeholder':'CATEGORY','style':'color:gray;'}),
        'description':forms.Textarea(attrs={'class':'form-control','placeholder':'description','style':'resize: none;'}),
        'price':forms.NumberInput(attrs={'class':'form-control','placeholder':'price'}),
        'image_1':forms.FileInput(attrs={'class':'form-control','style':'padding-top: 1em; padding-left: 1.5em;'}),
        'image_2':forms.FileInput(attrs={'class':'form-control','style':'padding-top: 1em; padding-left: 1.5em;'}),
        'availablity_status':forms.Select(attrs={'class':'form-control disabled','placeholder':'availibility status',"style":" border: 1px solid #eee;color:gray;"},choices=st),
        }
    def __init__(self, *args, **kwargs):
        super(NewPost, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "CATEGORY"

#-------------------------------------------New Blog Form-----------------------------------------------------

class NewBlog(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['posted_by','posted_at']
        widgets={
       
        'subject':forms.TextInput(attrs={'class':'form-control','placeholder':'subject'}),
        'content':forms.Textarea(attrs={'class':'form-control','placeholder':'content','style':'resize: none;'}),
        'img':forms.FileInput(attrs={'class':'form-control','style':'padding-top: 1em; padding-left: 1.5em;'}),

        }


#-------------------------------------------FAQ Form----------------------------------------------------------

class FAQs(forms.ModelForm):

    class Meta:
        model=FAQ
        fields=['question']
        widgets={'question':forms.TextInput(attrs={'class':'form-control col-lg-12 mb-3','placeholder':'Question ?'})}

#-----------------------------------------Edit FAQ Form--------------------------------------------------------------

class EditFAQs(forms.ModelForm):
    class Meta:
        model=FAQ
        fields=['question','answer']
        widgets={
        'question':forms.TextInput(attrs={'class':'form-control col-lg-12 mb-3','placeholder':'Question ?','readonly':'readonly'}),
        'answer':forms.Textarea(attrs={'class':'form-control col-lg-12 mb-3','placeholder':'Type Answer Here....','style':'resize: none;'})}

#-------------------------------------------Contact Us Form-----------------------------------------------------------

class ContactUsForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        fields=['name','email','subject','message']
        widgets={
        'name':forms.TextInput(attrs={'class':'form-control col-lg-12 mb-3','placeholder':'name'}),
        'email':forms.EmailInput(attrs={'class':'form-control col-lg-12 mb-3','placeholder':'email'}),
        'subject':forms.TextInput(attrs={'class':'form-control col-lg-12 mb-3','placeholder':'subject'}),
        'message':forms.Textarea(attrs={'class':'form-control col-lg-12 mb-3','placeholder':'Message','style':'resize: none;'})
        }

#--------------------------------------------Checkout Form----------------------------------------------------------

class CheckoutForm(forms.ModelForm):
    class Meta:
        model=CustomerContact
        fields=['contact_no','address','city','state','zip']
        widgets={
        'city':forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'city'}),
        'state':forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'state'}),
        'contact_no':forms.NumberInput(attrs={'class':'form-control mb-3','placeholder':'CONTACT'}),
        'zip':forms.NumberInput(attrs={'class':'form-control mb-3','placeholder':'zip number'}),
        'address':forms.Textarea(attrs={'class':'form-control mb-3','placeholder':'ADDRESS','style':'resize: none;height:11vh;'})
        }


#-------------------------------------------Change Password Form-----------------------------------------------------

class ChangePassUser(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Old password'}),label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New password'}),label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}),label='Re-enter Password')
    fields = ['old_password','new_password1','new_password2']


#-------------------------------------------Password Reset Form-----------------------------------------------------

class PassResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))

class SetNewPassword(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'New password'}),label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'}),label='Re-enter Password')
