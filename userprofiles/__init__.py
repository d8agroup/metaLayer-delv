
def _check_password_rules(new_password):
    """
    Verify that the given password matches the rules for this site.
    
    """
    
    if len(new_password) < 6:
        return False, [constants.PASSWORD_TOO_SHORT]
    
    return True, []