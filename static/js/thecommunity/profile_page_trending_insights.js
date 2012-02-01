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
            insight_container.profile_page_insight(dashboards[d]);
            insight_container.profile_page_insight('render_thumbnail');
        }
    };

    $.fn.profile_page_trending_insights = function()
    {
        var trensing_insights = this;
        $.get('/community/trending_insights/9', function(data) { render(data, trensing_insights); }, 'JSON');
    }
})(jQuery);