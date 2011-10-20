from django.http import HttpResponse, Http404
from django.utils import simplejson
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.db import models
import inputs.sources as sources
import datetime
import inspect
import re

################################################################################
# Methods for accessing and loading widgets dynamically                        #
################################################################################ 
def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def run_widget_url(request, widget_type, widget_name, function_name):
    try:
        return getattr(my_import('%s.%s.views' % (widget_type, widget_name)), function_name)(request)
    except AttributeError:
        raise Http404
    
def get_widget_data_by_widget_type(widget_type):
    if widget_type == 'inputwidgets':
        return [getattr(obj(), 'source_data')() for name, obj in inspect.getmembers(sources) if inspect.isclass(obj) and not issubclass(obj, models.Model)]
    else:
        return [getattr(my_import('%s.views' % name), 'widget_data')() for name in settings.INSTALLED_APPS if re.search(r'%s' % widget_type, name)]
    
def get_config_ensuring_collection(request, collection_id):
    all_collections_config = get_collection_config(request)
    if collection_id not in all_collections_config['collections']:
        all_collections_config['collections'][collection_id] = { 'inputs':[], 'actions':[] }
    return all_collections_config

def set_collection_config(request, config):
    request.session['collection_config'] = simplejson.dumps(config)
    
def get_collection_config(request):
    config = simplejson.loads(request.session['collection_config'] if 'collection_config' in request.session else '{"collections":{}}')
    return config 

def save_widget_config(request, collection, widget_type, widget_id, config):
    widget_config = request.session['widget_config'] if 'widget_config' in request.session else {}
    if not collection in widget_config:
        widget_config[collection] = {}
    if not widget_type in widget_config[collection]:
        widget_config[collection][widget_type] = {}
    widget_config[collection][widget_type][widget_id] = config
    request.session['widget_config'] = widget_config

def get_widget_config(request, collection, widget_type, widget_id):
    widget_config = request.session.get('widget_config')
    if not widget_config:
        return None
    if not collection in widget_config:
        return None
    if not widget_type in widget_config[collection]:
        return None      
    if not widget_id in widget_config[collection][widget_type]:
        return None
    return simplejson.loads(widget_config[collection][widget_type][widget_id])

def reconfigure_widget(request, collection, widget_type, widget_id):
    widget_config = request.session.get('widget_config')
    if not widget_config:
        return None
    if not collection in widget_config:
        return None
    if not widget_type in widget_config[collection]:
        return None      
    if not widget_id in widget_config[collection][widget_type]:
        return None
    widget_config[collection][widget_type].pop(widget_id)
    request.session['widget_config'] = widget_config
    
    
    

################################################################################
# JSON Response: http://chronosbox.org/blog/jsonresponse-in-django?lang=en     #
################################################################################ 
class LazyJSONEncoder(simplejson.JSONEncoder):
    """ a JSONEncoder subclass that handle querysets and models objects. Add
    your code about how to handle your type of object here to use when dumping
    json """
    def default(self,o):
        # this handles querysets and other iterable types
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
 
        # this handlers Models
        try:
            isinstance(o.__class__,ModelBase)
        except Exception:
            pass
        else:
            return force_unicode(o)
 
        return super(LazyJSONEncoder,self).default(o)
 
def serialize_to_json(obj,*args,**kwargs):
    """ A wrapper for simplejson.dumps with defaults as:
 
    ensure_ascii=False
    cls=LazyJSONEncoder
 
    All arguments can be added via kwargs
    """
    kwargs['ensure_ascii'] = kwargs.get('ensure_ascii',False)
    kwargs['cls'] = kwargs.get('cls',LazyJSONEncoder)
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
    return simplejson.dumps(obj, default=dthandler, *args,**kwargs)

class JSONResponse(HttpResponse):
    """ JSON response class """
    def __init__(self,content='',json_opts={},mimetype="application/json",
                 *args,**kwargs):
        """
        This returns a object that we send as json content using 
        utils.serialize_to_json, that is a wrapper to simplejson.dumps
        method using a custom class to handle models and querysets. Put your
        options to serialize_to_json in json_opts, other options are used by
        response.
        """
        if content:
            content = serialize_to_json(content,**json_opts)
        else:
            content = serialize_to_json([],**json_opts)
        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)
        
def format_template_and_json_response(template, context, data):
    template = get_template(template)
    html = template.render(Context(context))
    try:
        data = data.__dict__
    except AttributeError:
        data = data
    return_data = { "template":html, "data": data }
    return JSONResponse(return_data)