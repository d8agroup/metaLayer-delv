import constants

def _check_password_rules(new_password):
    """
    Verify that the given password matches the rules for this site.
    
    """
    
    if len(new_password) < 6:
        return False, [constants.USER_MESSAGES['password_too_short']]
    
    return True, []