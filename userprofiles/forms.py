from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.tokens import default_token_generator
from captcha.fields import ReCaptchaField
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlsafe_base64_encode
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

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("E-mail"), max_length=75)
    captcha = ReCaptchaField()

    def clean_email(self):
        """
        Validates that an active user exists with the given e-mail address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(
                                email__iexact=email,
                                is_active=True
                            )
        if len(self.users_cache) == 0:
            raise forms.ValidationError(_("That e-mail address doesn't have an associated user account. Are you sure you've registered?"))
        return email

    def save(self, domain_override=None, email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator, from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the user
        """
        from django.core.mail import send_mail
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            t = loader.get_template(email_template_name)
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(str(user.id)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            send_mail(_("Password reset on %s") % site_name,
                t.render(Context(c)), from_email, [user.email])