class BaseAction(object):
    def validate_config(self, config):
        return True, []

    def generate_configured_display_name(self, config):
        return config['display_name_long']

    def action_added(self, config):
        pass

    def action_removed(self, config):
        pass