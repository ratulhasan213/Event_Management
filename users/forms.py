from django import forms

from events.forms import StyledFormMixin
from users.models import Participant
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth import authenticate



class UserForm(StyledFormMixin,forms.ModelForm):
     
     confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password"
      )
     class Meta:
          model = User
          fields = ['username', 'email', 'first_name', 'last_name', 'password']
      
          widgets ={
                      "password": forms.PasswordInput()        
                  }
          



     def clean_username(self):
          username = self.cleaned_data.get('username')
          errors = []

          if User.objects.filter(username__iexact=username).exists():
               errors.append("User name already exists")
          
          if " " in username:
               errors.append("User name can't contain space")
           

          if errors:
            raise forms.ValidationError(errors)
      
          return username
     



     def clean_email(self):
        email = self.cleaned_data.get('email')
        errors = []
        
        if '@' not in email:
            errors.append("Email must contain @ sign")
        
        if User.objects.filter(email__iexact=email).exists():
            errors.append("Email already exists")
        

        if errors:
            raise forms.ValidationError(errors)
    
        return email
     
     

     def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []

        if not password:
            errors.append("Password cannot be empty")

        if len(password) < 8 :
            errors.append("The password must be at least 8 char long")
        
        if not any(char.isalpha() for char in password):
            errors.append("The password must contain a letter")
        if not any(dig.isdigit() for dig in password):
            errors.append("The password must contain a number")
        
        if errors:
            raise forms.ValidationError(errors)
        
        return password
      



      
     def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        errors = []


        if password:
            if password != confirm_password:
                  errors.append("passwords do not match")
        
        if errors:
            raise forms.ValidationError(errors)
        
        return cleaned_data
     

     
     


class ParticipantModelForm(StyledFormMixin,forms.ModelForm):
      class Meta:
            model = Participant
            fields = ["participantPhoto","phone_number"]

            widgets ={
                      "phone_number": forms.TextInput()        
                  }
        
      def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        errors = []
        
        if phone_number:
            qs = Participant.objects.filter(phone_number__iexact=phone_number)

            if self.instance.pk:
                qs = qs.exclude(pk = self.instance.pk)
            
            if qs.exists():
                errors.append("Phone number already exists")
        

        if errors:
            raise forms.ValidationError(errors)
    
        return phone_number
            




class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self,*args,**kargs):
            super().__init__(*args,**kargs)
      
     
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("Username or Password is incorrect")

        self.user_cache = user
        return cleaned_data
    

    

class UserEditForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_username(self):
    
        username = self.cleaned_data.get('username')
        errors = []

        if username:
            qs = User.objects.filter(username__iexact=username)

            if self.instance.pk:
                qs = qs.exclude(pk = self.instance.pk)
        
            if qs.exists():
                errors.append("User name already exists")
                
        if errors:
            raise forms.ValidationError(errors)
    
        return username
     



    def clean_email(self):
        email = self.cleaned_data.get('email')
        errors = []
        
        if '@' not in email:
            errors.append("Email must contain @ sign")



        if email:
            qs = User.objects.filter(email__iexact=email)

            if self.instance.pk:
                qs = qs.exclude(pk = self.instance.pk)
        
            if qs.exists():
                errors.append("Email already exists")

        if errors:
            raise forms.ValidationError(errors)
    
        return email




class AssignRoleForm(StyledFormMixin, forms.Form):

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_superuser=False),
        widget = forms.CheckboxSelectMultiple,
        label="Users"
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role",
        label="Role"
    )



class ChangeRoleForm(StyledFormMixin,forms.ModelForm):
    
     class Meta:
        model = Participant
        fields = []
     
     group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a role",
        label="Change Role"
    )
   
     



# class CreateGroupForm(StyledFormMixin,forms.ModelForm):
#     permissions = forms.ModelMultipleChoiceField(
#         queryset = Permission.objects.all(),
#         widget = forms.CheckboxSelectMultiple,
#         required = False,
#         label = "Assign Permission"
#     )

#     class Meta:
#         model = Group
#         fields = ['name','permissions']



#This is from chatgpt:

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("content_type"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Assign Permission"
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['permissions'].label_from_instance = (
            lambda perm: f"{perm.name} ({perm.content_type.app_label}.{perm.codename})"
        )



class ChangePasswordForm(StyledFormMixin,PasswordChangeForm):
     
      def clean_old_password(self):
          
          errors = []
          
          old_password = self.cleaned_data.get("old_password")
          if not self.user.check_password(old_password):
              errors.append("Old password is incorrect")

          if errors:
            raise forms.ValidationError(errors)
              
              
          return old_password
      
      
      def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        errors = []

        if new_password1 != new_password2:
            errors.append("New passwords do not match.")  

        if new_password1 and  len(new_password1) < 8 :
            errors.append("The password must be at least 8 char long")
    
        if not any(char.isalpha() for char in new_password1):
            errors.append("The password must contain a letter")

        if not any(dig.isdigit() for dig in new_password1):
            errors.append("The password must contain a number")


        if errors:
            raise forms.ValidationError(errors)

        
        return cleaned_data
          
    



class PasswordResetMyForm(StyledFormMixin,PasswordResetForm):
    pass


class PasswordResetConfirmForm(StyledFormMixin,SetPasswordForm):
    def clean_password(self):
        password = self.cleaned_data.get('new_password1')
        errors = []

        if len(password) < 8 :
            errors.append("The password must be at least 8 char long")
        
        if not any(char.isalpha() for char in password):
            errors.append("The password must contain a letter")
        if not any(dig.isdigit() for dig in password):
            errors.append("The password must contain a number")
        
        if errors:
            raise forms.ValidationError(errors)
        
        return password


             