/***********************************************************************************************************************
 DASHBOARD - dashboard_search_widget
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
            data_points_summary_html.append('<li><a><img src="' + data_points[x].image + '" /></a></li>');
            var data_point_detail_html = $("<li>" +
                                            "<img src='" + data_points[x].image + "' />" +
                                            "<span class='display_name'>" + data_points[x].configured_display_name + "</span>" +
                                            "<span class='actions'>" +
                                                "<a class='configure_data_point'>" +
                                                    "<img src='/static/images/site/icon_config.png'/>" +
                                                "</a>" +
                                            "</span>" +
                                        "</li>");
            data_point_detail_html.find('.configure_data_point').data('data_point', data_points[x])
            data_points_details_html.append(data_point_detail_html);
        }

        search_widgets_data_points.append(data_points_summary_html);
        search_widgets_data_points.append(data_points_details_html);

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
                        search_widgets_data_points.parents('.collection_container').dashboard_collection('render');
                    }
                )
            }
        );

        return this;
    };
})( jQuery );

/***********************************************************************************************************************
 DASHBOARD - dashboard_search_widget
***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function()
        {
            this.dashboard_search_widget('render');
            return this;
        },
        render:function()
        {
            var configuration = this.parents('.collection_container').data('configuration');

            var data_points = configuration.data_points;
            var data_points_container_html = $("<div class='data_points_container'></div>");
            this.append(data_points_container_html.dashboard_search_widget_data_points(data_points));

            var search_filters = configuration.search_filters;

            return this;
        }
    }

    $.fn.dashboard_search_widget = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );