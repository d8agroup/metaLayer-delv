from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from emails.utils import base_template_data
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def email_list(request):
    template_data = base_template_data()
    return render_to_response(
        'emails/email_listing_page.html',
        template_data,
        context_instance=RequestContext(request)
    )

def view_invite(request):
    template_data = base_template_data()
    template_data['invitee'] = 'mg@metalayer.com'
    template_data['code'] = 'TESTCODE_1'
    template_data['email'] = 'mg@metalayer.com'
    return render_to_response(
        'emails/email_templates/invite_01.html',
        template_data
    )


def test_email(request, email_type, recipient):
    template_data = base_template_data()
    if email_type == 'invite':
        template_data['invitee'] = 'mg@metalayer.com'
        subject = 'You have been invited to join metaLayer'
        from_email = 'Team Metalayer <no-reply@metalayer.com>'
        template_data['code'] = 'TESTCODE_1'
        template_data['email'] = 'mg@metalayer.com'
        html = render_to_string(
            'emails/email_templates/invite_01.html',
            template_data
        )
        text = strip_tags(html)
        msg = EmailMultiAlternatives(subject, text, from_email, [recipient])
        msg.attach_alternative(html, "text/html")
        msg.send()
        messages.info(request, 'That email has been sent')
        return redirect(email_list)
    raise Http404

def send_email(request, email_id):
    email_config = settings.EMAILS[email_id]
    return getattr(email_view_functions, email_config['view_function'])(request, email_id)