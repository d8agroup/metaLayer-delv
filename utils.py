from threading import Thread
from django.db.models.base import ModelBase
from django.http import HttpResponse
from django.utils import simplejson
from django.template.loader import get_template
from django.template import Context
import datetime

################################################################################
# ASYNC REQUESTS                                                               #
################################################################################
def async(gen):
    def func(*args, **kwargs):
        it = gen(*args, **kwargs)
        result = it.next()
        Thread(target=lambda: list(it)).start()
        return result
    return func

################################################################################
# DYNAMIC MODULE LOADED FUNCTIONS                                              #
################################################################################
from django.utils.encoding import force_unicode

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

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
