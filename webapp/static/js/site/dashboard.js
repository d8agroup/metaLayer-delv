/***********************************************************************************************************************
DASHBOARD - widgets panel
***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var widgets = data.widgets;
            this.children().remove();
            var empty_widget_panel_html = "<div id='widget_panel'><div class='widget data_point_widget'><p class='hidden type'>twitter</p><p class='hidden sub_type'>search</p>twitter</div></div>";
            this.html(empty_widget_panel_html);
            this.dashboard_widget_panel('apply_widget_draggable');
            return this;
        },
        apply_widget_draggable:function()
        {
            this.find('.data_point_widget').draggable
            (
                {
                    revert:true,
                    helper:"clone",
                    start:function()
                    {
                        $('#collections').dashboard_collections_panel('data_point_start_dragging');
                    },
                    stop:function()
                    {
                        $('#collections').dashboard_collections_panel('data_point_stop_dragging');
                    }
                }
            );
        }
    }

    $.fn.dashboard_widget_panel = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );

/***********************************************************************************************************************
DASHBOARD - collections panel
***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            this.children().remove();
            var collections = data.collections;
            var collection_class = 'collections_' + collections.length;
            for (collection in collections)
            {
                var collection_container_html = '<div class="collection_container ' + collection_class + '"></div>';
                var collection_container = $(collection_container_html).dashboard_collection({ collection:collections });
                this.append(collection_container);
            }
            return this;
        },
        data_point_start_dragging:function()
        {
            this.find('.collection_container').dashboard_collection('data_point_start_dragging');
        },
        data_point_stop_dragging:function()
        {
            this.find('.collection_container').dashboard_collection('data_point_stop_dragging');
        }
    }

    $.fn.dashboard_collections_panel = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );

/** DASHBOARD - collection ********************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var collection = data.collection;
            this.data('configuration', collection);
            this.dashboard_collection('render');
            return this;
        },
        render:function()
        {
            var configuration = this.data('configuration');
            if (configuration.data_points == null || configuration.data_points.length == 0)
            {
                var empty_collection_html = "<div class='empty_collection data_point_droppable'><p>Drag & Drop Data</p></div>";
                this.html(empty_collection_html);
            }
            else
            {

                var search_widget_container_html = $("<div class='search_widget data_point_droppable'></div>");
                this.html(search_widget_container_html);

                var unconfigured_data_point = null;
                for (var x=0; x<configuration.data_points.length; x++)
                    if (!configuration.data_points[x].configured)
                        unconfigured_data_point = configuration.data_points[x];

                if (unconfigured_data_point != null)
                {
                    search_widget_container_html.dashboard_unconfigured_data_point(unconfigured_data_point);
                    return;
                }
            }
            this.dashboard_collection('apply_data_point_droppable');
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
                        var draggable_type = draggable.find('.type').html();
                        var draggable_sub_type = draggable.find('.sub_type').html();
                        if (configuration.data_points == null)
                            configuration['data_points'] = [];
                        configuration.data_points[configuration.data_points.length] =
                        {
                            id:guid(),
                            type:draggable_type,
                            sub_type:draggable_sub_type,
                            configured:false
                        };
                        collection.data('configuration', configuration);
                        collection.dashboard_collection('render');
                    }
                }
            )
        },
        remove_data_point:function(data_point_id)
        {
            var collection = this;
            var configuration = collection.data('configuration');
            var new_configuration = configuration;
            new_configuration.data_points = [];
            for (var x=0; x<configuration.data_points.length; x++)
                if (configuration.data_points[x].id != data_point_id)
                    new_configuration.data_points[new_configuration.data_points.length] = configuration.data_points[x];
            collection.data('configuration', new_configuration);
            collection.dashboard_collection('render');
        }
    };

    $.fn.dashboard_collection = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );

/** DASHBOARD - unconfigured data point *******************************************************************************/
(function( $ )
{
    $.fn.dashboard_unconfigured_data_point = function(unconfigured_data_point)
    {
        var search_widget_container = this;
        var id = unconfigured_data_point.id;
        var type = unconfigured_data_point.type;
        var sub_type = unconfigured_data_point.sub_type;
        search_widget_container.load
        (
            '/dashboard/render/data_point_config/' + type + '/' + sub_type,
            function()
            {
                var configuration = search_widget_container.find('.data_point_config').data('configuration');
                search_widget_container.find('.data_point_config form .cancel').click
                (
                    function()
                    {
                        search_widget_container.parents('.collection_container').dashboard_collection('remove_data_point', id);
                        return search_widget_container;
                    }
                );
            }
        );
    }
})( jQuery );

/***********************************************************************************************************************
DASHBOARD
***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var dashboard = data.dashboard;
            this.find('#widgets').dashboard_widget_panel({widgets:dashboard.widgets});
            this.find('#collections').dashboard_collections_panel({'collections':dashboard.collections})
        }
    }

    $.fn.dashboard = function( method ) {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' ); }
})( jQuery );