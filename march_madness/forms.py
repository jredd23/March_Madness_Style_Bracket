from django import forms
from django.contrib.auth.models import User

class POSTForm(forms.Form):
    username = forms.CharField(
	label='Username', 
	max_length=30, 
	help_text='Enter a unique name for your login',
	widget=forms.TextInput(attrs={
	    'required': 'required',
	    'title': 'Enter a unique name for your login',
	    'data-toggle': "tooltip",
	    'data-placement': "right",
	})
    )
    first_name = forms.CharField(
	label='First Name', 
	max_length=30,
        widget=forms.TextInput(attrs={
            'required': 'required',
            'title': 'Enter your First Name',
            'data-toggle': "tooltip",
            'data-placement': "right",
        })
	)
    last_name = forms.CharField(
	label='Last Name', 
	max_length=30,
        widget=forms.TextInput(attrs={
            'required': 'required',
            'title': 'Enter your Last Name',
            'data-toggle': "tooltip",
            'data-placement': "right",
        })
	)
    email = forms.EmailField(
	label='E-Mail Address', 
	max_length=75,
        widget=forms.EmailInput(attrs={
            'required': 'required',
            'title': 'Enter your email address to receive verification of submissions and updates',
            'data-toggle': "tooltip",
            'data-placement': "right",
        })
	)
    password = forms.CharField(
	label="Password", 
	max_length=128, 
	widget=forms.PasswordInput(attrs={
	    'required': 'required',
    	})
	)
    password2 = forms.CharField(
	label="Verify Password", 
	max_length=128, 
	widget=forms.PasswordInput(attrs={
	    'required': 'required',    
            'title': 'Passwords Must match',
            'data-toggle': "tooltip",
            'data-placement': "right",
	})
	)

    def clean(self):
        form_data = super(POSTForm, self).clean()
        if form_data['password'] != form_data['password2']:
            msg = "Passwords do not Match"
            self.add_error( 'password', msg)
