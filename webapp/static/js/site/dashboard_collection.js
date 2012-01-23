/***********************************************************************************************************************
 dashboard_collection - CHECKED 19/01/2012
 ***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var dashboard_collection = this;
            var collection = data.collection;
            if (collection.options == null)
                collection.options = {};
            if (collection.search_filters == null)
                collection.search_filters = {};
            if (collection.search_results == null)
                collection.search_results = {};
            if (collection.data_points == null)
                collection.data_points = [];
            if (collection.actions == null)
                collection.actions = [];
            if (collection.outputs == null)
                collection.outputs = [];
            dashboard_collection.data('configuration', collection);
            dashboard_collection.dashboard_collection('render');
            return dashboard_collection;
        },
        render:function()
        {
            var dashboard_collection = this;
            var configuration = dashboard_collection.data('configuration');
            if (configuration.data_points.length == 0)
            {
                var empty_collection_html = "<div class='empty_collection data_point_droppable'><p>Drag & Drop Data</p></div>";
                dashboard_collection.html(empty_collection_html);
            }
            else
            {
                var search_widget_html = $("<div class='search_widget data_point_droppable action_droppable output_droppable'></div>");
                dashboard_collection.html(search_widget_html);
                search_widget_html.dashboard_search_widget(configuration);

                if (configuration.outputs.length > 0)
                {
                    var outputs_container_html = $("<div class='outputs_container output_droppable'></div>");
                    outputs_container_html.dashboard_outputs(configuration);
                    dashboard_collection.append(outputs_container_html);
                }

                dashboard_collection.draggable( { revert:true, stack:'.collection_container', handle:'.search_widget' } );
            }
            dashboard_collection.dashboard_collection('apply_dashboard_collection_droppable');
            dashboard_collection.dashboard_collection('apply_data_point_droppable');
            dashboard_collection.dashboard_collection('apply_action_droppable');
            dashboard_collection.dashboard_collection('apply_output_droppable');
            $('#dashboard').dashboard('save');
            return dashboard_collection;
        },
        remove:function()
        {
            var dashboard_collection = this;
            var configuration = dashboard_collection.data('configuration');
            configuration.options = {};
            configuration.search_filters = {};
            configuration.search_results = {};
            configuration.data_points = [];
            configuration.actions = [];
            for (var o=0; o<configuration.outputs.length; o++)
                $.post( '/dashboard/outputs/remove_output', { output:JSON.stringify(configuration.outputs[o]), csrfmiddlewaretoken:$('#csrf_form input').val() } );
            configuration.outputs = [];
            dashboard_collection.dashboard_collection('render');
            return dashboard_collection;
        },
        apply_dashboard_collection_droppable:function()
        {
            var collection_dropped_function = function(event, ui, collection, configuration)
            {
                var dragged_collection = ui.draggable;
                var dragged_configuration = dragged_collection.data('configuration');
                if (dragged_configuration.data_points.length == 0)
                    return;
                for (var x=0; x<dragged_configuration.data_points.length; x++)
                    configuration.data_points[configuration.data_points.length] = dragged_configuration.data_points[x];
                $(dragged_collection).dashboard_collection('remove');
                collection.dashboard_collection('render');
            };

            var collection = this;
            var configuration = collection.data('configuration');
            collection.droppable
                (
                    {
                        accept:'.collection_container',
                        drop:function(event, ui) { collection_dropped_function(event, ui, collection, configuration); }
                    }
                );
        },
        apply_data_point_droppable:function()
        {
            var data_point_dropped_function = function(event, ui, configuration, collection)
            {
                var draggable = ui.draggable;
                var data_point = clone(draggable.data('data_point'));
                data_point['id'] = guid();
                if (configuration.data_points == null)
                    configuration['data_points'] = [];
                configuration.data_points[configuration.data_points.length] = data_point;
                collection.data('configuration', configuration);
                collection.dashboard_collection('render');
            };

            var collection = this;
            var configuration = collection.data('configuration');
            collection.find('.data_point_droppable').droppable
                (
                    {
                        accept:'.data_point_widget',
                        drop:function(event, ui) { data_point_dropped_function(event, ui, configuration, collection); }
                    }
                );
            return this;
        },
        apply_action_droppable:function()
        {
            var action_dropped_function = function(event, ui, configuration, collection)
            {
                var draggable = ui.draggable;
                var action = clone(draggable.data('action'));
                action['id'] = guid();
                if (configuration.actions == null)
                    configuration.actions = [];
                configuration.actions[configuration.actions.length] = action;
                collection.data('configuration', configuration);
                collection.dashboard_collection('render');
            };

            var collection = this;
            var configuration = collection.data('configuration');
            collection.find('.action_droppable').droppable
                (
                    {
                        accept:'.action_widget',
                        drop:function(event, ui) { action_dropped_function(event, ui, configuration, collection); }
                    }
                );
            return this;
        },
        apply_output_droppable:function()
        {
            var output_dropped_function = function(event, ui, configuration, collection)
            {
                var process_get_url_function = function(data, configuration, collection)
                {
                    var output = data.output;
                    if (configuration.outputs == null)
                        configuration.outputs = [];
                    configuration.outputs[configuration.outputs.length] = output;
                    collection.data('configuration', configuration);
                    collection.dashboard_collection('render');
                };

                var draggable = ui.draggable;
                var output = clone(draggable.data('output'));
                output['id'] = guid();
                output['collection_id'] = configuration.id;
                output['dashboard_id'] = $('#dashboard').data('dashboard').id;
                $.post
                    (
                        '/dashboard/outputs/get_url',
                        { output:JSON.stringify(output), csrfmiddlewaretoken:$('#csrf_form input').val()},
                        function(data) { process_get_url_function(data, configuration, collection); }
                    );
            };

            var collection = this;
            var configuration = collection.data('configuration');
            collection.find('.output_droppable').droppable
                (
                    {
                        accept:'.output_widget',
                        drop:function(event, ui) { output_dropped_function(event, ui, configuration, collection); }
                    }
                );
            return this;
        },
        remove_output:function(output_id)
        {
            var collection = this;
            var configuration = collection.data('configuration');
            var new_outputs = [];
            for (var x=0; x<configuration.outputs.length; x++)
                if (configuration.outputs[x].id != output_id)
                    new_outputs[new_outputs.length] = configuration.outputs[x];
                else
                    $.post
                        (
                            '/dashboard/outputs/remove_output',
                            { output:JSON.stringify(configuration.outputs[x]), csrfmiddlewaretoken:$('#csrf_form input').val() }
                        );
            collection.data('configuration').outputs = new_outputs;
            collection.dashboard_collection('render');

            return collection;
        }
    };

    $.fn.dashboard_collection = function( method )
    {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.dashboard_collection' );
    }
})( jQuery );