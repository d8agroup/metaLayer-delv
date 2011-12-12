from django import template
import re
register = template.Library()
 
@register.filter("truncate_chars")
def truncate_chars(value, max_length):
    if len(value) <= max_length:
        return value
 
    truncd_val = value[:max_length]
    #if value[max_length] != " ":
        #rightmost_space = truncd_val.rfind(" ")
        #if rightmost_space != -1:
            #truncd_val = truncd_val[:rightmost_space]
 
    return truncd_val + "..."

@register.filter('is_url')
def is_url(value):
    return re.search('http', value)
