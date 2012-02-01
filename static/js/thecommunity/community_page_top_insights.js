(function( $ )
{
    var render = function(data, container)
    {
        var top_insights = data.top_insights;
        container.find('ul').children().remove();
        for (var x=0; x<top_insights.length; x++)
        {
            if (x == 0)
            {
                var top_insight_container = container.find('#top_insight_container');
                top_insight_container.insight(top_insights[x]);
                top_insight_container.insight('render_medium');
            }
            else
            {
                var li = $('<li></li>');
                container.find('ul').append(li);
                li.insight(top_insights[x]);
                li.insight('render_thumbnail');
            }
        }
    };

    $.fn.community_page_top_insights = function()
    {
        var community_page_top_insights = this;
        $.get
            (
                '/community/top_insights/4',
                function(data) { render(data, community_page_top_insights); },
                'JSON'
            );
    }
})(jQuery);