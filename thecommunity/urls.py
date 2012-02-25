from django.conf.urls.defaults import patterns, url
from django.contrib.auth.views import password_reset, password_reset_confirm, \
        password_reset_complete, password_reset_done
from dashboard.userprofiles.forms import SetPasswordForm
from dashboard.thecommunity.views import *

urlpatterns = patterns('',
    url(r'restricted_access$', no_access),
    url(r'restricted_access/with_code$', no_access_with_code),
    url(r'welcome$', login_or_register),
    url(r'logout', logout),
    url(r'password_reset$', password_reset,
        {   
            'template_name': 'thecommunity/password_reset/password_reset_form.html', 
            'email_template_name': 'thecommunity/password_reset/password_reset_email.html',
            'is_admin_site': True   # setting this parameter causes OOB logic to pull domain from META.HTTP_HOST in settings
                                    # instead of from Sites (which will throw an exception)
                                    # see django.contrib.auth.views:password_reset line 153-154
        }),
    url(r'reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, 
        { 
            'template_name': 'thecommunity/password_reset/password_reset_confirm.html',
            'set_password_form': SetPasswordForm
        }),
    url(r'password_reset_done$', password_reset_done, 
        { 
            'template_name': 'thecommunity/password_reset/password_reset_done.html'
        }),
    url(r'password_reset_success$', password_reset_complete, 
        { 
            'template_name': 'thecommunity/password_reset/password_reset_complete.html'
        }),
    url(r'current_subscription', current_subscription),
    url(r'change_subscription', change_subscription),
    url(r'change_password$', change_password),
    url(r'change_email_opt_in$', change_email_opt_in),
    url(r'save_facebook_profile$', link_facebook_profile),
    url(r'create_from_template$', create_from_template),
    url(r'insights/load/([a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})$', load_dashboards),
    url(r'insights/load/([a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})/(\d+)$', load_dashboards),
    url(r'trending_insights/(\d+)$', load_tending_insights),
    url(r'top_insights/(\d+)$', load_top_insights),
    url(r'recent_insights/(\d+)$', load_recent_insights),
    url(r'remixes/(\w{24})/(\d+)$', load_remixes),
    url(r'delete_insight/(\w{24})$', delete_insight),
    url(r'[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}/account$', user_account),
    url(r'([a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})$', user_home),
    url(r'([a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6})/(\w{24})$', insight),
    url(r'([\w ]+)', category_page),
    url(r'^$', community_page),
)