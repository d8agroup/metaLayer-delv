import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

from controllers import UserController
from django.contrib.auth.models import User
import constants

test_user = test_user2 = test_user3 = None
controller = controller2 = controller3 = None

def setup():
    
    global test_user, test_user2, test_user3
    global controller, controller2, controller3
    
    test_user = User.objects.create_user('todd.mcneal.test1@gmail.com', 'todd.mcneal.test1@gmail.com', 'password')
    test_user2 = User.objects.create_user('todd.mcneal.test2@gmail.com', 'todd.mcneal.test2@gmail.com', 'password')
    test_user3 = User.objects.create_user('todd.mcneal.test3@gmail.com', 'todd.mcneal.test3@gmail.com', 'password')
    controller = UserController(test_user)
    controller2 = UserController(test_user2)
    controller3 = UserController(test_user3)
    
    #atest = User.objects.get_or_create(username='todd.mcneal@gmail.com')[0]
    #atest.set_password('password')
    #atest.save()
    
def test_password_incorrect():
    
    passed, errors = controller.change_password('wrong_password', 'new_password', 'new_password')
    
    assert not passed
    assert constants.USER_MESSAGES['password_incorrect'] in errors, errors

def test_password_mismatch():
    
    passed, errors = controller.change_password('password', 'new_password', 'new_password1')
    
    assert not passed
    assert constants.USER_MESSAGES['new_password_mismatch'] in errors, errors

def test_new_password_too_short():
    
    passed, errors = controller.change_password('password', 'short', 'short')
    
    assert not passed
    assert constants.USER_MESSAGES['password_too_short'] in errors, errors

def test_change_password_success():
    
    passed, errors = controller.change_password('password', 'password', 'password')
    
    assert passed

def test_passwords_blank():
    
    passed, errors = controller.change_password('', '', '')
    
    assert not passed
    assert constants.USER_MESSAGES['new_password_blank'] in errors, errors
    assert constants.USER_MESSAGES['confirm_password_blank'] in errors, errors
    assert constants.USER_MESSAGES['password_blank'] in errors, errors

def test_get_profile_image_none():
    
    assert test_user.profile.profile_image() == None, test_user.profile.profile_image()

def test_link_facebook_profile_missing_facebook_id():
    
    passed, errors = controller.link_facebook_profile('', 'bogus_access_token')
    
    assert not passed
    assert constants.USER_MESSAGES['facebook_id_missing'] in errors, errors

def test_link_facebook_profile_missing_access_token():
    
    passed, errors = controller.link_facebook_profile('bogus_facebook_id', None)
    
    assert not passed
    assert constants.USER_MESSAGES['facebook_access_token_missing'] in errors, errors

def test_link_facebook_profile_success():
    
    # Note that we don't validate that facebook id and access token are legit
    facebook_id = 'bogus_fb_id'
    access_token = 'bogus_access_token'
    
    passed, errors = controller2.link_facebook_profile(facebook_id, access_token)
    
    assert passed
    assert test_user2.profile.profile_image() == 'graph.facebook.com/%s/picture?type=normal' % facebook_id, test_user.profile.profile_image()

def test_link_twitter_profile_missing_screen_name():
    
    passed, errors = controller.link_twitter_profile(None)
    
    assert not passed
    assert constants.USER_MESSAGES['twitter_screen_name_missing'] in errors, errors

def test_link_twitter_profile_success():
    
    twitter_handle = 'bogus_screen'
    
    passed, errors = controller3.link_twitter_profile(twitter_handle)
    
    assert passed
    assert test_user3.profile.profile_image() == 'api.twitter.com/1/users/profile_image/%s?type=large' % twitter_handle

def test_link_facebook_and_twitter_success():
    
    facebook_id = 'bogus_fb'
    twitter_handle = 'bogus_twitter'
    
    passed, errors = controller.link_facebook_profile(facebook_id, 'bogus_access')
    
    assert passed
    
    passed, errors = controller.link_twitter_profile(twitter_handle)
    
    assert passed
    
    assert test_user.profile.linked_via_facebook()
    assert test_user.profile.linked_via_twitter()
    assert test_user.profile.profile_image() == 'graph.facebook.com/%s/picture?type=normal' % facebook_id, test_user.profile.profile_image()

def test_email_opt_in_missing_status():
    
    passed, errors = controller.change_email_opt_in(None)
    
    assert not passed
    assert constants.USER_MESSAGES['opt_in_status_missing'] in errors, errors

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

