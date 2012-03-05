"""
Constants used by the userprofiles application.

"""

# change password
USER_DOES_NOT_EXIST = 'The user does not exist in the system'
PASSWORD_BLANK = 'Password can not be blank'
NEW_PASSWORD_BLANK = 'New password can not be blank'
CONFIRM_PASSWORD_BLANK = 'Confirmed password can not be blank'
NEW_PASSWORD_MISMATCH = 'Confirmed password does not match new password'
PASSWORD_INCORRECT = 'Sorry, the password you entered is incorrect'
PASSWORD_TOO_SHORT = 'Your password must be at least 6 characters long'

# link facebook profile
FACEBOOK_ID_MISSING = 'Facebook ID is missing from request'
FACEBOOK_ACCESS_TOKEN_MISSING = 'Facebook access token is missing from request'

# link twitter profile
TWITTER_SCREEN_NAME_MISSING = 'Twitter screen name is missing from request'

# user options
OPT_IN_STATUS_MISSING = 'Opt-in status is missing from request'
