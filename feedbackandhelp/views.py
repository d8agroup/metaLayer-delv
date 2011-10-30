from django.http import HttpResponse
from django.shortcuts import render_to_response

def give_feedback(request):
    sent = False
    if request.method == 'POST':
        from django.core.mail import EmailMessage
        email = EmailMessage('Message from the Dashboard - MVP', '%s [%s]: %s' % (request.POST['name'], request.POST['email'], request.POST['feedback']), to=['mg@metalayer.com'])
        email.send()
        sent = True
    return render_to_response('givefeedback.html', { 'sent':sent })