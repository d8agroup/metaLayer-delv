from core.utils import get_collection_config
from core.utils import my_import
import inputs.sources as sources
from Queue import Queue
import threading

def run_all_inputs_and_combine_results(inputs):
    def producer(q, _inputs):
        for _input in _inputs:
            thread = InputRunner(_input)
            thread.start()
            q.put(thread, True)
 
    finished = []
    
    def consumer(q, total_files):
        while len(finished) < total_files:
            thread = q.get(True)
            thread.join()
            finished.append(thread.get_result())
 
    q = Queue()
    prod_thread = threading.Thread(target=producer, args=(q, inputs))
    cons_thread = threading.Thread(target=consumer, args=(q, len(inputs)))
    prod_thread.start()
    cons_thread.start()
    prod_thread.join()
    cons_thread.join()    

    all_content = []
    
    for results in finished:
        for result in results:
            all_content.append(result)
    
    """
    for input in inputs:
        source_bridge = getattr(sources, input['type'])()
        for content in source_bridge.run_for_input(input):
            all_content.append(content)
    """
    
    all_content = sorted(all_content, key=lambda item: -1 * item['time'])
    return all_content

def apply_actions(request, collection_id, content, actions):
    for action in actions:
        views = my_import('actionwidgets.%s.views' % action['type'])
        function = getattr(views, 'run_action_for_content')
        content = function(request, collection_id, action['id'], content)
    return content

class InputRunner(threading.Thread):
    def __init__(self, input):
        self.input = input
        self.result = None
        threading.Thread.__init__(self)
    
    def get_result(self):
        return self.result
    
    def run(self):
        source_bridge = getattr(sources, self.input['type'])()
        self.result = source_bridge.run_for_input(self.input)
        
