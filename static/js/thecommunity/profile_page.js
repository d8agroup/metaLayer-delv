(function( $ ){
    var methods =
    {
        init:function()
        {
            this.profile_page('render');
        },
        render:function()
        {
            var profile_page = this;
            profile_page.find('#start_new_insight').button();
            profile_page.find('#my_creations').profile_page_my_creations();
            profile_page.find('#trending_insights').insights_trending_insights(9);
            profile_page.find('#insights_timeline #timeline').profile_page_insights_timeline();
        }
    };

    $.fn.profile_page = function(method)
    {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.profile_page_insights_timeline_insight_container' );
    }
})( jQuery );