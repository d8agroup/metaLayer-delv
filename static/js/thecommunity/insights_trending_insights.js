(function( $ )
{
    var render = function(data, container)
    {
        container.find('ul').children().remove();
        var dashboards = data.trending_insights;
        for (var d=0; d<dashboards.length; d++)
        {
            var insight_container = $('<li></li>');
            container.find('ul').append(insight_container);
            insight_container.insight(dashboards[d]);
            insight_container.insight('render_thumbnail');
        }
    };

    $.fn.insights_trending_insights = function(count)
    {
        var trensing_insights = this;
        $.get('/community/trending_insights/' + count, function(data) { render(data, trensing_insights); }, 'JSON');
    }
})(jQuery);