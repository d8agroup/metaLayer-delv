import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

from controllers import UserController
from django.contrib.auth.models import User
import constants

mock_request = None
test_user = None
controller = None

def setup():
    
    global test_user, controller, mock_request
    
    mock_request = 'mock_request'
    test_user = User.objects.create_user('todd.mcneal.test1@gmail.com', 'todd.mcneal.test1@gmail.com', 'password')
    controller = UserController(test_user)
    

def test_password_incorrect():
    
    passed, errors = controller.change_password(mock_request, 'wrong_password', 'new_password', 'new_password')
    
    assert not passed
    assert constants.PASSWORD_INCORRECT in errors, errors

def test_password_mismatch():
    
    passed, errors = controller.change_password(mock_request, 'password', 'new_password', 'new_password1')
    
    assert not passed
    assert constants.NEW_PASSWORD_MISMATCH in errors, errors

def test_new_password_too_short():
    
    passed, errors = controller.change_password(mock_request, 'password', 'short', 'short')
    
    assert not passed
    assert constants.PASSWORD_TOO_SHORT in errors, errors

def test_change_password_success():
    
    passed, errors = controller.change_password(mock_request, 'password', 'password', 'password')
    
    assert passed

def test_passwords_blank():
    
    passed, errors = controller.change_password(mock_request, '', '', '')
    
    assert not passed
    assert constants.NEW_PASSWORD_BLANK in errors, errors
    assert constants.CONFIRM_PASSWORD_BLANK in errors, errors
    assert constants.PASSWORD_BLANK in errors, errors

def test_remove_linked_accounts():
    
    user = User.objects.get_or_create(username='todd.mcneal@gmail.com')[0]
    profile = user.profile
    
    profile.linked_accounts = {}
    profile.save()
    
    assert profile.linked_accounts == {}
    
