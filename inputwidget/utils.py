from core.utils import get_collection_config
import inputs.sources as sources


def get_config_ensuring_collection(request, collection_id):
    all_collections_config = get_collection_config(request)
    if collection_id not in all_collections_config['collections']:
        all_collections_config['collections'][collection_id] = { 'inputs':[] }
    return all_collections_config


def run_all_inputs_and_combine_results(inputs):
    all_content = []
    for input in inputs:
        source_bridge = getattr(sources, input['type'])()
        for content in source_bridge.run_for_input(input):
            all_content.append(content)
    all_content = sorted(all_content, key=lambda item: -1 * item['time'])
    return all_content