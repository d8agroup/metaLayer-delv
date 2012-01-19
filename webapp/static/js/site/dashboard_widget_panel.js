/***********************************************************************************************************************
 DASHBOARD - widgets panel - CHECKED 18/01/2012
 ***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var render_data_points_function = function(data, widget_panel)
            {
                var load_data_point_content_template = function(data)
                {
                    var template = data.template;
                    var template_name = 'dashboard_search_results_content_items_' + data.type + '_' + data.sub_type;
                    $.template(template_name, template);
                };

                var empty_widget_panel_html = $("<div id='widget_panel'></div>");
                var data_points = data.data_points;
                for (var x=0; x<data_points.length; x++)
                {
                    var data_point = data_points[x];
                    var data_point_html = $('<div class="data_point_widget">' + data_point.short_display_name + '</div>');
                    data_point_html.data('data_point', data_point);
                    empty_widget_panel_html.append(data_point_html);
                    data_point_html.corner();

                    //Also load the content item templates
                    var load_template_url = '/dashboard/data_points/get_content_item_template/' + data_point.type + '/' + data_point.sub_type;
                    $.get ( load_template_url, function(data) { load_data_point_content_template(data); } );
                }
                widget_panel.html(empty_widget_panel_html);
                widget_panel.dashboard_widget_panel('apply_widget_draggable');
            };

            var widget_panel = this;
            widget_panel.children().remove();
            $.get ( '/dashboard/data_points/get_all', function(data) { render_data_points_function(data, widget_panel) }, 'JSON' );
            return widget_panel;
        },
        apply_widget_draggable:function()
        {
            var widget_panel = this;
            widget_panel.find('.data_point_widget').draggable( { revert:true, helper:"clone", stack:'.collection_container' });
            return widget_panel;
        }
    };

    $.fn.dashboard_widget_panel = function( method )
    {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.dashboard_widget_panel' );
    }
})( jQuery );