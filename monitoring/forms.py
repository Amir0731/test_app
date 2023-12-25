from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm, UserChangeForm, \
    ReadOnlyPasswordHashField
from django.core.exceptions import ObjectDoesNotExist

from django.forms import ModelForm, inlineformset_factory, HiddenInput
from django.utils.translation import gettext_lazy as _

from monitoring.models import MainResult, InfoResult, User, Variant, Exercise


# from monitoring.models import Student


class SubjectAddForm(forms.Form):
    subject_name = forms.CharField(widget=forms.TextInput(attrs={'required': True}), max_length=100, required=False,
                                   label='Fanni kiriting')


class SignUpForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = None
        try:
            try:
                user = User.objects.get(username=username)
                print("is user active username", user.is_active)
            except ObjectDoesNotExist as e:
                pass
            except Exception as e:
                raise e
            if not user:
                pass
            elif not user.is_active:
                pass
            else:
                raise forms.ValidationError(_("Bunday foydalanuvchi taxallusiga ega foydalanuvchi mavjud."))
        except Exception as e:
            raise e
        return username

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        # self.fields["username"].label = ''
        self.fields["username"].help_text = None
        self.fields["username"].widget.attrs.update(
            {"placeholder": _("Foydalanuvchi taxalusi..."), 'class': 'form-control'})

        #         self.fields["first_name"].label = ''
        self.fields["first_name"].help_text = None
        self.fields["first_name"].widget.attrs.update({"placeholder": _("Ism..."), 'class': 'form-control'})

        #         self.fields["last_name"].label = ''
        self.fields["last_name"].help_text = None
        self.fields["last_name"].widget.attrs.update({"placeholder": _("Familiya..."), 'class': 'form-control'})

        #         self.fields["password1"].label = ''
        self.fields["password1"].help_text = None
        self.fields["password1"].widget.attrs.update({"placeholder": _("Parol..."), 'class': 'form-control'})

        #         self.fields["password2"].label = ''
        self.fields["password2"].help_text = None
        self.fields["password2"].widget.attrs.update(
            {"placeholder": _("Parolni takrorlang..."), 'class': 'form-control'})

        #         self.fields["email"].label = ''
        self.fields["email"].help_text = None
        self.fields["email"].widget.attrs.update({'required': True})
        self.fields["email"].widget.attrs.update({"placeholder": _("Elektron pochta..."), 'class': 'form-control'})

        self.error_messages['password_mismatch'] = _('Parollar bir xil bo\'lishi shart!')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', "password2")


class InglizchaErrorChiqarmaslik(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(InglizchaErrorChiqarmaslik, self).__init__(*args, **kwargs)
        self.fields['username'].label = _('Foydalanuvchi taxalusi')
        self.fields['username'].widget.attrs.update({"placeholder": _("Foydalanuvchi taxalusi...")})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        # self.fields['password'].label = ''
        self.fields['password'].widget.attrs.update({"placeholder": _("Parol...")})
        self.fields['password'].widget.attrs.update({"class": 'form-control'})

    error_messages = {
        'invalid_login': _('Login yoki parol xato.')
    }


# select modelni formasi
"""
class TestForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
"""


class MainResultForm(ModelForm):
    class Meta:
        model = MainResult
        fields = ['user_id', 'username', 'subject_name', 'subject_id', 'subject_variant', 'subject_variant_id']


class InfoResultForm(ModelForm):
    class Meta:
        model = InfoResult
        fields = ['user_id', 'username', 'subject_name', 'subject_id', 'subject_variant', 'subject_variant_id',
                  'exercise_id',
                  'exercise_text', 'user_selected_variant_id',
                  'is_resolved_true']


class VariantForm(ModelForm):
    class Meta:
        model = Variant
        fields = ['title', 'title_uz', 'title_ru', 'title_en']


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'

        # widgets = {'text': {'class': 'form-control'}}


ExerciseFormSet = inlineformset_factory(
    Variant,
    Exercise,
    fields=[
        'text', 'text_uz', 'text_ru', 'text_en',
    ],
    extra=1,
    can_delete=False
)


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        # self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': _("Foydalanuvchi taxalusi...")})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Ism...')})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Familiya...')})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': _('Familiya...')})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        # fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'avatar')
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar']
