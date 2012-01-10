/** DASHBOARD - collection ********************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var collection = data.collection;

            if (collection.options == null)
                collection.options = {};

            if (collection.search_filters == null)
                collection.search_filters = {};

            if (collection.search_results == null)
                collection.search_results = {};

            if (collection.data_points == null)
                collection.data_points = [];

            this.data('configuration', collection);
            this.dashboard_collection('render');
            return this;
        },
        render:function()
        {
            var configuration = this.data('configuration');
            if (configuration.data_points.length == 0)
            {
                var empty_collection_html = "<div class='empty_collection data_point_droppable'><p>Drag & Drop Data</p></div>";
                this.html(empty_collection_html);
            }
            else
            {
                var search_widget_container_html = $("<div class='search_widget_container data_point_droppable'></div>");
                this.html(search_widget_container_html);

                for (var x=0; x<configuration.data_points.length; x++)
                    if (!configuration.data_points[x].configured)
                    {
                        search_widget_container_html.dashboard_unconfigured_data_point(configuration.data_points[x]);
                        return this;
                    }

                var search_widget_html = $("<div class='search_widget'></div>");
                search_widget_container_html.html(search_widget_html);
                search_widget_html.dashboard_search_widget(configuration);
                setTimeout
                (
                    function()
                    {
                        $.post
                        (
                            '/dashboard/run_search',
                            {
                                data_points:JSON.stringify(configuration.data_points),
                                search_filters:JSON.stringify(configuration.search_filters),
                                csrfmiddlewaretoken:$('#csrf_form input').val()
                            },
                            function(data)
                            {
                                var search_results = data.search_results;
                                configuration.search_results = search_results;
                                search_widget_html.dashboard_search_widget('search_results_updated');
                            }
                        )
                    },
                    1000
                );
            }
            this.dashboard_collection('apply_data_point_droppable');
            $('#dashboard').dashboard('save');
            return this;
        },
        remove:function()
        {
            var configuration = this.data('configuration');
            configuration.options = {};
            configuration.search_filters = {};
            configuration.search_results = {};
            configuration.data_points = [];
            return this.dashboard_collection('render');
        },
        data_point_start_dragging:function()
        {
            this.find('.data_point_droppable').addClass('data_point_droppable_active');
        },
        data_point_stop_dragging:function()
        {
            this.find('.data_point_droppable').removeClass('data_point_droppable_active');
        },
        apply_data_point_droppable:function()
        {
            var collection = this;
            var configuration = collection.data('configuration');
            collection.find('.data_point_droppable').droppable
            (
                {
                    accept:'.data_point_widget',
                    drop:function(event, ui)
                    {
                        var draggable = ui.draggable;
                        var data_point = clone(draggable.data('data_point'));
                        data_point['id'] = guid();
                        if (configuration.data_points == null)
                            configuration['data_points'] = [];
                        configuration.data_points[configuration.data_points.length] = data_point;
                        collection.data('configuration', configuration);
                        collection.dashboard_collection('render');
                    }
                }
            );
        },
        remove_data_point:function(data_point_id)
        {
            var configuration = this.data('configuration');
            var new_data_points = [];
            for (var x=0; x<configuration.data_points.length; x++)
                if (configuration.data_points[x].id != data_point_id)
                    new_data_points[new_data_points.length] = configuration.data_points[x];
            this.data('configuration').data_points = new_data_points;
            return this;
        }
    };

    $.fn.dashboard_collection = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );