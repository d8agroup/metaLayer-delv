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
                var search_widget_html = $("<div class='search_widget data_point_droppable'></div>");
                dashboard_collection.html(search_widget_html);
                search_widget_html.dashboard_search_widget(configuration);
                dashboard_collection.draggable( { revert:true, stack:'.collection_container' } );
            }
            dashboard_collection.dashboard_collection('apply_dashboard_collection_droppable');
            dashboard_collection.dashboard_collection('apply_data_point_droppable');
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
        }
    };

    $.fn.dashboard_collection = function( method )
    {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.dashboard_collection' );
    }
})( jQuery );