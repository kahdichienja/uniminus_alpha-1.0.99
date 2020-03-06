from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from student.models import StudentProfile
from stuff.models import StudentProfileAttribute, StudentUnit

class StudentProfileAttributeForm(forms.ModelForm):
    """Form definition for StudentProfileAttribute."""
    # department = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'mdl-textfield__input', 'id': 'department','tabIndex': '-1', 'readonly': 'true', 'required': 'true'}))
    accademic_year = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'id': 'accademic_year','tabIndex': '-1', 'readonly': 'true', 'required': 'true'}))
    year_of_study = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'id': 'year_of_study','tabIndex': '-1', 'readonly': 'true', 'required': 'true'}))
    student_session = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'id': 'student_session','tabIndex': '-1', 'readonly': 'true', 'required': 'true'}))
    picture = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'dropzone','id': 'picture', 'accept':'image/*', 'required': 'true'}))
    study_method = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'id': 'study_method','tabIndex': '-1', 'readonly': 'true', 'required': 'true'}))
    # program = forms.CharField(widget=forms.TextInput(
    #     attrs={'class': 'mdl-textfield__input', 'id': 'program','tabIndex': '-1', 'readonly': 'true', 'required': 'true'}))
    class Meta:
        """Meta definition for StudentProfileAttributeform."""

        model = StudentProfileAttribute
        fields = ['study_method','accademic_year','year_of_study','student_session','picture']

class StudentProfileForm(forms.ModelForm):
    """Form definition for StudentProfile."""
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'id': 'first_name', 'required': 'true'}))
    surname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'id': 'surname', 'required': 'true'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'id': 'last_name', 'required': 'true'}))
    adm_number = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'mdl-textfield__input', 'id': 'adm_number', 'required': 'true'}))

    class Meta:
        """Meta definition for StudentProfileform."""

        model = StudentProfile
        fields = ['first_name','surname','last_name','adm_number']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'input100', 'id': 'id_email', 'placeholder': 'Email programme', 'required': 'true'}))
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'id': 'id_username', 'placeholder':'Username', 'required': 'true'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input100', 'id': 'id_password1','placeholder':'Password', 'required': 'true'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input100', 'id': 'id_password2','placeholder':'Confirm Password', 'required': 'true'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input100', 'id': 'id_username', 'placeholder':'Username', 'required': 'true'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input100', 'id': 'id_password', 'placeholder':'Password','required': 'true'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # user_qs = User.objects.filter(username=username)
        # if user_qs.count() == 1:
        #     user = user_qs.first()
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(
                    "This user Does Not exists in the system")
            if not user.check_password(password):
                raise forms.ValidationError("Password Incorrect")
            if not user.is_active:
                raise forms.ValidationError(
                    "User Is No longer Active. Contact Admin 254797324006")
        return super(UserLoginForm, self).clean(*args, **kwargs)
