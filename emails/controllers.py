from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from emails.utils import base_template_data

class EmailController(object):
    @classmethod
    def SendInviteEmail(cls, to_user, code, from_user=None):
        template_data = base_template_data()
        template_data['invitee'] = from_user
        subject = 'You have been invited to join DeLv from metaLayer'
        from_email = 'Team Metalayer <no-reply@metalayer.com>'
        template_data['code'] = code
        template_data['email'] = to_user
        html = render_to_string(
            'emails/email_templates/invite_01.html',
            template_data
        )
        text = strip_tags(html)
        msg = EmailMultiAlternatives(subject, text, from_email, [to_user])
        msg.attach_alternative(html, "text/html")
        msg.send()