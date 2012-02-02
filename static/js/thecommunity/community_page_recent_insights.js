(function( $ )
{
    var render = function(data, container)
    {
        var recent_insights = data.recent_insights;
        container.find('ul').children().remove();
        for (var x=0; x<recent_insights.length; x++)
        {
            var li = $('<li></li>');
            container.find('ul').append(li);
            li.insight(recent_insights[x]);
            li.insight('render_thumbnail');
        }
    };

    $.fn.community_page_recent_insights = function()
    {
        var community_page_recent_insights = this;
        $.get
            (
                '/community/recent_insights/8',
                function(data) { render(data, community_page_recent_insights); },
                'JSON'
            );
    }
})(jQuery);