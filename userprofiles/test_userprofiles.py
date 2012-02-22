import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

from controllers import UserController
from django.contrib.auth.models import User
import constants

test_user = None
controller = None

def setup():
    
    global test_user, controller
    
    test_user = User.objects.create_user('todd.mcneal.test1@gmail.com', 'todd.mcneal.test1@gmail.com', 'password')
    controller = UserController(test_user)
    
    #atest = User.objects.get_or_create(username='todd.mcneal@gmail.com')[0]
    #atest.set_password('password')
    #atest.save()
    
def test_password_incorrect():
    
    passed, errors = controller.change_password('wrong_password', 'new_password', 'new_password')
    
    assert not passed
    assert constants.PASSWORD_INCORRECT in errors, errors

def test_password_mismatch():
    
    passed, errors = controller.change_password('password', 'new_password', 'new_password1')
    
    assert not passed
    assert constants.NEW_PASSWORD_MISMATCH in errors, errors

def test_new_password_too_short():
    
    passed, errors = controller.change_password('password', 'short', 'short')
    
    assert not passed
    assert constants.PASSWORD_TOO_SHORT in errors, errors

def test_change_password_success():
    
    passed, errors = controller.change_password('password', 'password', 'password')
    
    assert passed

def test_passwords_blank():
    
    passed, errors = controller.change_password('', '', '')
    
    assert not passed
    assert constants.NEW_PASSWORD_BLANK in errors, errors
    assert constants.CONFIRM_PASSWORD_BLANK in errors, errors
    assert constants.PASSWORD_BLANK in errors, errors

def test_get_profile_image_none():
    
    assert test_user.profile.profile_image() == None, test_user.profile.profile_image()

def test_link_facebook_profile_missing_facebook_id():
    
    passed, errors = controller.link_facebook_profile('', 'bogus_access_token')
    
    assert not passed
    assert constants.FACEBOOK_ID_MISSING in errors, errors

def test_link_facebook_profile_missing_access_token():
    
    passed, errors = controller.link_facebook_profile('bogus_facebook_id', None)
    
    assert not passed
    assert constants.FACEBOOK_ACCESS_TOKEN_MISSING in errors, errors

def test_link_facebook_profile_success():
    
    # Note that we don't validate that facebook id and access token are legit
    facebook_id = 'bogus_fb_id'
    access_token = 'bogus_access_token'
    
    passed, errors = controller.link_facebook_profile(facebook_id, access_token)
    
    assert passed
    assert test_user.profile.profile_image() == 'graph.facebook.com/%s/picture?type=normal' % facebook_id, test_user.profile.profile_image()

def test_email_opt_in_missing_status():
    
    passed, errors = controller.change_email_opt_in(None)
    
    assert not passed
    assert constants.OPT_IN_STATUS_MISSING in errors, errors

def test_email_opt_in_success():
    
    passed, errors = controller.change_email_opt_in('Y')
    
    assert passed
    assert test_user.profile.email_opt_in() == True

def test_email_opt_out_success():
    
    passed, errors = controller.change_email_opt_in('N')
    
    assert passed
    assert test_user.profile.email_opt_in() == False

def teardown():
    
    test_user.delete()

"""
def test_remove_linked_accounts():
    
    user = User.objects.get_or_create(username='todd.mcneal@gmail.com')[0]
    profile = user.profile
    
    profile.linked_accounts = {}
    profile.save()
    
    assert profile.linked_accounts == {}
"""

