class RegistrationPolicy(object):
    def post_registration(self, user, registration_form_values):
        user_profile = user.profile
        user_profile.registration_status = 'WAITING'
        user_profile.save()