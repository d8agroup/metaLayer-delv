/***********************************************************************************************************************
 DASHBOARD - dashboard_search_widget_data_points
 ***********************************************************************************************************************/
(function( $ )
{
    $.fn.dashboard_search_widget_data_points = function(data_points)
    {
        var search_widgets_data_points = this;

        var data_points_summary_html = $('<ul class="data_points_summary"></ul>');
        var data_points_details_html = $("<ul class='data_points_details hidden'></ul>");

        for (var x=0; x<data_points.length; x++)
        {
            data_points_summary_html.append
            (
                '<li>' +
                    '<a>' +
                        '<img src="' + data_points[x].image_small + '" title="' + data_points[x].configured_display_name + '" />' +
                    '</a>' +
                '</li>'
            );

            var data_point_detail_html =  $
            (
                "<li>" +
                    "<img src='" + data_points[x].image_small + "' />" +
                    "<span class='display_name'>" + data_points[x].configured_display_name + "</span>" +
                    "<span class='actions'>" +
                        "<a class='configure_data_point'>" +
                            "<img src='/static/images/site/icon_config.png'/>" +
                        "</a>" +
                    "</span>" +
                "</li>"
            );
            data_point_detail_html.find('.configure_data_point').data('data_point', data_points[x])
            data_points_details_html.append(data_point_detail_html);
        }

        search_widgets_data_points.append(data_points_summary_html);
        search_widgets_data_points.append(data_points_details_html);

        Tipped.create(search_widgets_data_points.find('.data_points_summary img'));

        search_widgets_data_points.find('.data_points_summary a').click
            (
                function()
                {
                    search_widgets_data_points.find('.data_points_summary').slideUp();
                    search_widgets_data_points.find('.data_points_details').slideDown().mouseleave
                        (
                            function()
                            {
                                setTimeout
                                    (
                                        function()
                                        {
                                            search_widgets_data_points.find('.data_points_summary').slideDown();
                                            search_widgets_data_points.find('.data_points_details').slideUp();
                                        },
                                        2000
                                    );
                            }
                        );
                }
            );

        search_widgets_data_points.find('.data_points_details .actions .configure_data_point').each
            (
                function()
                {
                    var data_point = $(this).data('data_point');
                    $(this).click
                        (
                            function()
                            {
                                data_point.configured = false;
                                $.post('/dashboard/data_points/remove_data_point', { data_point:JSON.stringify(data_point), csrfmiddlewaretoken:$('#csrf_form input').val() })
                                search_widgets_data_points.parents('.collection_container').dashboard_collection('render');
                            }
                        )
                }
            );

        return this;
    };
})( jQuery );
