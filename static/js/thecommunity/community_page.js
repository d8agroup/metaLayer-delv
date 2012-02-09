(function( $ )
{
    $.fn.community_page = function()
    {
        var community_page = this;
        $('#top_insights_inner').community_page_top_insights();
        $('#recent_activity').community_page_recent_insights();
        $('#trending_insights').insights_trending_insights(8);
        Tipped.create(community_page.find('#brows_by_category a'));
    }
})(jQuery);