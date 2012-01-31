(function( $ )
{
    var render_insight_timeline = function(data, container)
    {
        container.children().remove();
        var dashboards = data.dashboards;
        for (var x=0; x<dashboards.length; x++)
        {
            var insight_container = $('<li class="dashboard"></li>');
            container.append(insight_container);
            insight_container.profile_page_insights_timeline_insight_container(dashboards[x]);
        }
    }
    
    var methods =
    {
        init:function()
        {
            var insights_timeline = this;
            $.get('/community/insights/load', function(data) { render_insight_timeline(data, insights_timeline); }, 'JSON');
        }
    };

    $.fn.profile_page_insights_timeline = function(method)
    {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.profile_page_insights_timeline' );
    };
})(jQuery);