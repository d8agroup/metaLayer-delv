from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from emails.utils import base_template_data
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def email_list(request):
    template_data = base_template_data()
    template_data['emails'] = settings.EMAILS.values()
    return render_to_response(
        'emails/email_listing_page.html',
        template_data,
        context_instance=RequestContext(request)
    )

def view_email(request, email_type):
    template_data = base_template_data()
    template_data['invitee'] = 'mg@metalayer.com'
    if email_type == 'invite_01':
        template_data['code'] = 'TESTCODE_1'
        template_data['email'] = 'mg@metalayer.com'
        return render_to_response(
            'emails/invite_01.html',
            template_data
        )
    raise Http404

def test_email(request, email_type, recipient):
    template_data = base_template_data()
    template_data['invitee'] = 'mg@metalayer.com'
    if email_type == 'invite_01':
        subject = 'You have been invited to join metaLayer'
        from_email = 'support@metalayer.com'
        template_data['code'] = 'TESTCODE_1'
        template_data['email'] = 'mg@metalayer.com'
        html = render_to_string(
            'emails/invite_01.html',
            template_data
        )
        text = strip_tags(html)
        msg = EmailMultiAlternatives(subject, text, from_email, [recipient])
        msg.attach_alternative(html, "text/html")
        msg.send()
        messages.info(request, 'That email has been sent')
        return redirect(email_list)
    raise Http404
