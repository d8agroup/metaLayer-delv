(function( $ )
{
    var render_my_creations = function(data, container)
    {
        container.find('ul').children().remove();
        var dashboards = data.dashboards;
        for (var d=0; d<dashboards.length; d++)
        {
            var insight_container = $('<li></li>');
            container.find('ul').append(insight_container);
            var visualization = null;
            var dashboard = dashboards[d];
            for (var x=0; x<dashboard.collections.length; x++)
                if (dashboard.collections[x].visualizations != null && dashboard.collections[x].visualizations.length > 0)
                    for (var y=0; y<dashboard.collections[x].visualizations.length; y++)
                        if (dashboard.collections[x].visualizations[y].configured)
                            visualization = dashboard.collections[x].visualizations[y].snapshot;
            if (visualization != null)
            {
                var visualization_container = $('<div class="my_creation_container"><canvas width="100px" height="75px"></canvas></div>');
                insight_container.append(visualization_container);
                canvg(insight_container.find('canvas')[0], visualization, { scaleWidth:100, scaleHeight:75, ignoreMouse:true});
            }
            else
            {
                var data_logos = [];
                for (var x=0; x<dashboard.collections.length; x++)
                    for (var y=0; y<dashboard.collections[x].data_points.length; y++)
                        if (data_logos.length < 9)
                            data_logos[data_logos.length] = dashboard.collections[x].data_points[y].image_small;
                var data_container = $('<div class="my_creation_container"></div>');
                insight_container.append(data_container);
                for (var y=0; y<data_logos.length; y++)
                    data_container.append("<img src='" + data_logos[y] + "' />");
                if (data_logos.length == 1)
                    data_container.addClass('one_image_row');
                else if (data_logos.length < 5)
                    data_container.addClass('two_image_row');
                else
                    data_container.addClass('three_image_row');
            }
            insight_container.corner();
        }

    }

    $.fn.profile_page_my_creations = function()
    {
        var my_creations = this;
        $.get('/community/insights/load', function(data) { render_my_creations(data, my_creations); }, 'JSON');
    }
})(jQuery);