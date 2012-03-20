from logger import Logger
from models import CommentFlag, Comment
from profanity import CURSE_WORDS
import re

class CommentsController(object):
    
    @classmethod
    def GetCommentById(cls, comment_id):
        Logger.Info('%s - CommentsController.GetCommentById - started' % __name__)
        Logger.Debug('%s - CommentsController.GetCommentById - comment_id:%s' 
                % (__name__, comment_id))
                
        comment = Comment.objects.get(id=comment_id)
        
        Logger.Info('%s - CommentsController.GetCommentById - finished' % __name__)
        return comment
    
    @classmethod
    def FlagInappropriate(cls, user_comment, flagging_user):
        Logger.Info('%s - CommentsController.FlagInappropriate - started' % __name__)
        Logger.Debug('%s - CommentsController.FlagInappropriate - user_comment:%s and flagging_user:%r' 
                % (__name__, user_comment, flagging_user))
        
        if CommentFlag.GetForCommentAndUser(user_comment, flagging_user):
            return False, ['Comment has already been flagged']
        
        comment_flag = CommentFlag(user_comment=user_comment, flagging_user=flagging_user)
        comment_flag.save()
        
        Logger.Info('%s - CommentsController.FlagInappropriate - finished' % __name__)
        return True, []
    
    @classmethod
    def CreateComment(cls, user, insight, comment):
        Logger.Info('%s - CommentsController.CreateComment - started' % __name__)
        Logger.Debug('%s - CommentsController.CreateComment - user:%r and insight:%r and comment:%s' 
                % (__name__, user, insight, comment))
        
        # check that comment is not empty
        if not comment or len(comment.strip()) == 0:
            return False, ['Comment is empty']
        
        # invoke profanity filter
        comment = cls._filter_profanity(comment)
        
        comment = Comment(user=user, comment=comment, insight=insight)
        comment.save()
        
        # Save number of comments associated with this insight
        if 'comments' in insight.community:
            insight.community['comments'] = insight.community['comments'] + 1
        else:
            insight.community['comments'] = 1
        insight.save()
        
        Logger.Info('%s - CommentsController.CreateComment - finished' % __name__)
        return True, []
    
    @classmethod
    def GetComments(cls, insight):
        Logger.Info('%s - CommentsController.GetComments - started' % __name__)
        Logger.Debug('%s - CommentsController.GetComments - insight:%r'
                % (__name__, insight))
        
        result = []
        try:
            comments = Comment.objects.filter(insight=insight)
            
            for comment in comments:
                
                # don't include comment if it has been flagged
                testt = CommentFlag.objects.filter(user_comment=comment)
                if len(testt) == 0:
                    result.append(comment)
            
        except Comment.DoesNotExist:
            pass
        
        Logger.Info('%s - CommentsController.GetComments - finished' % __name__)
        return result
    
    @classmethod
    def _filter_profanity(cls, comment):
        
        result = []
        
        splitter = re.compile(r'(\s+|\S+)')
        
        for word in splitter.findall(comment):
            if word.lower() in CURSE_WORDS:
                replacement = ''
                for x in range(len(word)):
                    replacement += '*'
                
                result.append(replacement)
            else:
                result.append(word)
        
        return ''.join(result)



