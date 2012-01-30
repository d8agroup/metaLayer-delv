(function( $ ){

    var methods =
    {
        init:function(dashboard)
        {
            var insight_container = this;
            insight_container.data('dashboard', dashboard);
            return insight_container.profile_page_insights_timeline_insight_container('render_short_summary');
        },
        render_short_summary:function()
        {
            var insight_container = this;
            var dashboard = insight_container.data('dashboard');

            //Check for the presence of visualizations to assign correct template
            for (var x=0; x<dashboard.collections.length; x++)
                if (dashboard.collections[x].visualizations.length > 0)
                    return insight_container.profile_page_insights_timeline_insight_container('_render_short_summary_for_visualization');
            return insight_container.profile_page_insights_timeline_insight_container('_render_short_summary_for_data');
        },
        _render_short_summary_for_visualization:function()
        {

        },
        _render_short_summary_for_data:function()
        {

        }
    };

    $.fn.profile_page_insights_timeline_insight_container = function(method)
    {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.profile_page_insights_timeline_insight_container' );
    }
})(jQuery);