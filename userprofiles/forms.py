from django import forms
from django.utils.translation import ugettext_lazy as _
from . import _check_password_rules
import constants

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without
    entering the old password.
    
    This is a replacement for django.contrib.auth.forms:SetPasswordForm.
    We've created our own form so that we can embed custom validation
    logic within it.
    
    """
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_("The two password fields didn't match."))
        
        passed, errors = _check_password_rules(password1)
        
        if not passed:
            raise forms.ValidationError(errors[0])
        
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user