import random
import string
from django.conf import settings
from emails.controllers import EmailController
from invites.models import Invite
from logger import Logger

class InviteController(object):
    @classmethod
    def InsightsRemainingForUser(cls, user):
        if not user.is_authenticated():
            return 0
        if user.is_staff:
            return 10
        invite_limit = settings.INVITES['per_user_limit']
        invites_sent = Invite.objects.filter(user=user).count()
        if invites_sent >= invite_limit:
            return 0
        return invite_limit - invites_sent
    
    @classmethod
    def SendInviteFromUser(cls, user, to_user_email):
        if not cls.InsightsRemainingForUser(user):
            return False
        invite = Invite(user=user, code='', to_email=to_user_email )
        code = "".join( [random.choice(string.letters[:26]) for i in xrange(5)] ).upper()
        while Invite.objects.filter(code=code).count():
            code = "".join( [random.choice(string.letters[:26]) for i in xrange(5)] ).upper()
        invite.code = code
        invite.save()
        try:
            EmailController.SendInviteEmail(to_user_email, invite.code, user.username)
        except Exception, e:
            Logger.Warn('%s - InviteController.SendInviteFromUser - error sending email' % __name__)
            Logger.Debug('%s - InviteController.SendInviteFromUser - error sending email: %s' % (__name__, e))
            invite.delete()
            return False
        return True
