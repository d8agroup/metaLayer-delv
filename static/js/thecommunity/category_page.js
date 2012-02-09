(function($)
{
    $.fn.category_page = function(data)
    {
        var category_page = this;
        var insight_list = category_page.find('#insight_list');
        insight_list.children().remove();
        var insights = data.insights;
        for (var x=0; x<insights.length; x++)
        {
            var insight_html = $("<li></li>");
            insight_list.append(insight_html);
            insight_html.insight(insights[x]);
            insight_html.insight('render_thumbnail');
        }
        return category_page;
    }
})(jQuery);