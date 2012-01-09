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
            var widget_panel = this;
            widget_panel.children().remove();
            var empty_widget_panel_html = $("<div id='widget_panel'></div>");

            $.get
            (
                '/dashboard/data_points/get_all',
                function(data)
                {
                    var data_points = data.data_points;
                    for (var x=0; x<data_points.length; x++)
                    {
                        var data_point_html = $('<div class="data_point_widget">' + data_points[x].short_display_name + '</div>');
                        data_point_html.data('data_point', data_points[x]);
                        empty_widget_panel_html.append(data_point_html);

                        //Also load the content item templates
                        $.get
                        (
                            '/dashboard/data_points/get_content_item_template/' + data_points[x].type + '/' + data_points[x].sub_type,
                            function(data)
                            {
                                var template = data.template;
                                var template_name = 'dashboard_search_results_content_items_' + data.type + '_' + data.sub_type;
                                $.template(template_name, template);
                            }
                        );
                    }
                    widget_panel.html(empty_widget_panel_html);
                    widget_panel.dashboard_widget_panel('apply_widget_draggable');
                },
                'JSON'
            );
            return widget_panel;
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