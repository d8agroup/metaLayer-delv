from django.conf import settings

def base_template_data():
    return {
        'site_host':settings.SITE_HOST,
        'image_host':settings.IMAGE_HOST,
    }