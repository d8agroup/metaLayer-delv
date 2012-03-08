import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

from controllers import CommentsController
from django.contrib.auth.models import User
from models import Comment, CommentFlag
from metalayercore.dashboards.models import Dashboard, DashboardTemplate

test_user = test_comment = test_dashboard = test_template = controller = None

def setup():
    
    global test_user, test_comment, test_dashboard, test_template, controller
    
    test_user = User.objects.create_user('todd.mcneal.test1@gmail.com', 'todd.mcneal.test1@gmail.com', 'password')
    test_template = DashboardTemplate.AllForUser(test_user)[0]
    test_dashboard = Dashboard.Create(user=test_user, template=test_template)
    test_dashboard.save()
    test_comment = Comment(user=test_user, comment='test_comment', insight=test_dashboard)
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

def test_retrieve_comments_no_comments():
    
    test_dashboard2 = Dashboard.Create(user=test_user, template=test_template)
    
    comments = CommentsController.GetComments(test_dashboard2)
    
    assert len(comments) == 0, len(comments)
    
def test_retrieve_comment_success():
    
    comments = CommentsController.GetComments(test_dashboard)
    
    assert len(comments) == 1, len(comments)

def test_write_comment_empty():
    
    success, errors = CommentsController.CreateComment(test_user, test_dashboard, '')
    
    assert not success
    assert 'Comment is empty' in errors, errors

def test_write_comment_success():
    
    success, errors = CommentsController.CreateComment(test_user, test_dashboard, 'my_test_comment')
    
    assert success

def teardown():
    pass


