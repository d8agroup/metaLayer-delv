from invites.controllers import InviteController

class RegistrationPolicy(object):
    def post_registration(self, user, registration_form_values):
        if 'register_code' not in registration_form_values or not registration_form_values['register_code']:
            return

        register_code = registration_form_values['register_code']
        register_code = register_code.upper()
        if not InviteController.AcceptUserRegistrationWithCode(register_code):
            return

        user_profile = user.profile
        user_profile.registration_code = 'INVITE - %s' % register_code
        user_profile.registration_status = 'APPROVED'
        user_profile.save()