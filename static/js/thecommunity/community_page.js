(function( $ )
{
    $.fn.community_page = function()
    {
        var community_page = this;
        $('#top_insights_inner').community_page_top_insights();
        $('#trending_insights').insights_trending_insights(8);
    }
})(jQuery);