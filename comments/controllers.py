from logger import Logger
from models import CommentFlag, Comment

class CommentsController(object):
    
    def __init__(self, user_comment):
        Logger.Info('%s - CommentsController - started' % __name__)
        Logger.Debug('%s - CommentsController - started with user_comment:%s' % (__name__, user_comment))
        self.user_comment = user_comment
        Logger.Info('%s - CommentsController - finished' % __name__)
    
    def flag_inappropriate(self, flagging_user):
        Logger.Info('%s - flag_inappropriate - started' % __name__)
        
        #TODO add user listed as inappropriate.. need this to be in join table
        
        if CommentFlag.GetForCommentAndUser(self.user_comment, flagging_user):
            return False, ['Comment already exists']
        
        comment_flag = CommentFlag(user_comment=self.user_comment, flagging_user=flagging_user)
        comment_flag.save()
        
        Logger.Info('%s - flag_inappropriate - finished' % __name__)
        return True, []
    
    @classmethod
    def CreateComment(cls, user, insight, comment):
        
        # check that comment is not empty
        if not comment or len(comment.strip()) == 0:
            return False, ['Comment is empty']
        
        #TODO invoke profanity filter here
        
        comment = Comment(user=user, comment=comment, insight=insight)
        comment.save()
        
        return True, []
    
    @classmethod
    def GetComments(cls, insight):
        try:
            return Comment.objects.filter(insight=insight)
        except Comment.DoesNotExist:
            return []