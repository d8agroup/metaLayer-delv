(function( $ ){
    $.fn.profile_page = function()
    {
        var profile_page = this;
        profile_page.find('.page_block').corner();
        profile_page.find('#start_new_insight').button();
        profile_page.find('#insights_timeline #timeline').profile_page_insights_timeline();
    };
})( jQuery );