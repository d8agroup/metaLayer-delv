(function( $ )
{
    var render_my_creations = function(data, container)
    {
        container.find('ul').children().remove();
        var dashboards = data.dashboards;
        for (var d=0; d<dashboards.length; d++)
        {
            var insight_container = $("<li></li>");
            container.find('ul').append(insight_container);
            insight_container.profile_page_insight(dashboards[d]);
            insight_container.profile_page_insight('render_thumbnail');
        }
    };

    $.fn.profile_page_my_creations = function()
    {
        var my_creations = this;
        var username = $('#page').data('username');
        $.get('/community/insights/load/' + username, function(data) { render_my_creations(data, my_creations); }, 'JSON');
    }
})(jQuery);