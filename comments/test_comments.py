import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

from controllers import CommentsController
from django.contrib.auth.models import User
from models import UserComment, CommentFlag

test_user = None
test_comment = None
controller = None

def setup():
    
    global test_user, test_comment, controller
    
    test_user = User.objects.create_user('todd.mcneal.test1@gmail.com', 'todd.mcneal.test1@gmail.com', 'password')
    test_comment = UserComment(user=test_user, comment='test_comment')
    test_comment.save()
    controller = CommentsController(test_comment)

def test_flag_inappropriate_duplicate_flag():
    
    flagging_user = User.objects.create_user('todd.mcneal.test2@gmail.com', 'todd.mcneal.test2@gmail.com', 'password')
    
    test = []
    
    success, errors = controller.flag_inappropriate(flagging_user)
    
    if not success:
        assert False, errors
    
    success, errors = controller.flag_inappropriate(flagging_user)
    
    if success:
        assert False, 'should have flagged this as a duplicate'

def teardown():
    pass