from inputwidget.utils import run_all_inputs_and_combine_results
from inputwidget.utils import apply_actions
from django.shortcuts import render_to_response
from django.http import HttpResponse
from core.utils import get_config_ensuring_collection
from core.utils import set_collection_config
from hashlib import md5
import datetime
import random
import xlwt

type = 'spreadsheet'

def widget_data():
    return { 'type':type, 'display_name':'Spreadsheet' }

def generate_unconfigured_config():
    return {
        'id':md5('%s' % random.random()).hexdigest(),
        'type':type, 
        'display_name':'Export to Spreadsheet',
        'config':{
            'configured':True,
            'elements':[]
        }
    }
    
def add_new(request):
    collection_id = request.GET['collection_id']
    config = get_config_ensuring_collection(request, collection_id)
    config['collections'][collection_id]['outputs'].append(generate_unconfigured_config())
    set_collection_config(request, config)
    return HttpResponse()

def remove(request):
    collection_id = request.GET['collection_id']
    id = request.GET['output_id']
    config = get_config_ensuring_collection(request, collection_id)
    print 'before', config
    config['collections'][collection_id]['outputs'] = [a for a in config['collections'][collection_id]['outputs'] if a['id'] != id]
    print 'after', config
    set_collection_config(request, config)
    return HttpResponse()

def render(collection_id, output_id):
    config = generate_unconfigured_config()
    config['id'] = output_id
    return render_to_response('spreadsheet_basic.html', { 'output':config, 'collection_id':collection_id })

def export(request):
    collection_id = request.GET['collection_id']
    config = get_config_ensuring_collection(request, collection_id)
    inputs = config['collections'][collection_id]['inputs']
    actions = config['collections'][collection_id]['actions']
    content = run_all_inputs_and_combine_results(inputs)
    content = apply_actions(request, collection_id, content, actions)
    
    
    xls = xlwt.Workbook()
    work_sheet_name = "MetaLayer-Export"
    ws = xls.add_sheet(work_sheet_name)
    ws.set_panes_frozen(True)
    ws.set_horz_split_pos(1)
    ws.set_remove_splits(True)

    header_row_style = xlwt.easyxf('font:bold on; pattern: pattern solid, fore-colour grey25')
    
    ws.write(0,0, 'Date Created', header_row_style)
    ws.write(0,1, 'Content Source', header_row_style)
    ws.write(0,2, 'Author', header_row_style)
    ws.write(0,3, 'Title', header_row_style)
    ws.write(0,4, 'Image', header_row_style)
    ws.write(0,5, 'Sentiment', header_row_style)
    ws.write(0,6, 'Tags', header_row_style)
    
    ws.col(0).width = max([len(datetime.datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %H:%M")) for i in content]) * 256
    ws.col(1).width = max([len(i['type']) for i in content] + [len('Content Source')]) * 256
    ws.col(2).width = max([len(i['author']) for i in content]) * 256
    ws.col(3).width = max([len(i['title']) for i in content]) * 256
    ws.col(4).width = max([len(i['image_url']) for i in content if 'image_url' in i] + [12]) * 256
    ws.col(5).width = max([len("%f" % i['sentiment']) for i in content if 'sentiment' in i] + [10]) * 256
    ws.col(6).width = max([len(' | '.join(i['tags'])) for i in content if 'tags' in i] + [10]) * 256
    
    row_count = 1
    for i in content:
        ws.write(row_count, 0, datetime.datetime.fromtimestamp(i['time']).strftime("%Y-%m-%d %H:%M"))
        ws.write(row_count, 1, i['type'])
        ws.write(row_count, 2, i['author'])
        ws.write(row_count, 3, i['title'])
        ws.write(row_count, 4, i['image_url'] if i['type'] in ['flickrsearch', 'twittersearch', 'twitteruser'] else '')
        ws.write(row_count, 5, i['sentiment'] if 'sentiment' in i else '')
        ws.write(row_count, 6, ' | '.join(i['tags']) if 'tags' in i else '')
        row_count = row_count + 1
        
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s-%s.xls' % (work_sheet_name, datetime.datetime.utcnow().strftime("%Y%m%d%H%M"))
    xls.save(response)
    return response
    

