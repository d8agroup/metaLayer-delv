"""
Model objects related to user comments and its associated functions, such as
the flagging of comments.

"""
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from logger import Logger


class UserComment(models.Model):
    user = models.ForeignKey(User)
    comment = models.TextField()
    created = models.DateTimeField(default=datetime.now)

class CommentFlag(models.Model):
    user_comment = models.ForeignKey(UserComment)
    flagging_user = models.ForeignKey(User)
    created = models.DateTimeField(default=datetime.now)
    
    @classmethod
    def GetForCommentAndUser(cls, user_comment, flagging_user):
        Logger.Info('%s - CommentFlag.GetForCommentAndUser - started' % __name__)
        Logger.Debug('%s - CommentFlag.GetForCommentAndUser - started with user_comment:%s and flagging_user:%s' % (__name__, user_comment, flagging_user))
        
        try:
            result = CommentFlag.objects.get(user_comment=user_comment, flagging_user=flagging_user)
        except CommentFlag.DoesNotExist:
            result = None
            
        Logger.Info('%s - CommentFlag.GetForCommentAndUser - finished' % __name__)
        return result
    
