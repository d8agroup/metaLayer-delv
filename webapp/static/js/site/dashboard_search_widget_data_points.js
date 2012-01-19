/***********************************************************************************************************************
 DASHBOARD - dashboard_search_widget_data_points - CHECKED 19/01/2012
 ***********************************************************************************************************************/
(function( $ )
{
    $.fn.dashboard_search_widget_data_points = function(data_points)
    {
        var data_point_clicked_function = function(link)
        {
            var data_point = link.data('data_point');
            data_point.configured = false;
            var post_data = { data_point:JSON.stringify(data_point), csrfmiddlewaretoken:$('#csrf_form input').val() };
            $.post('/dashboard/data_points/remove_data_point', post_data);
            link.parents('.collection_container').dashboard_collection('render');
        };

        var search_widgets_data_points = this;
        var data_points_summary_html = $('<ul class="data_points_summary"></ul>');
        for (var x=0; x<data_points.length; x++)
        {
            var data_point_html = $.tmpl('dashboard_search_widget_data_point', data_points[x]);
            data_point_html.find('a').data('data_point', data_points[x])
            data_point_html.find('a').click( function() { data_point_clicked_function($(this)); } );
            data_points_summary_html.append( data_point_html );
        }
        search_widgets_data_points.append(data_points_summary_html);
        return search_widgets_data_points;
    };
})( jQuery );
