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
            insight_container.profile_page_insight(dashboards[x]);
            insight_container.profile_page_insight('render_short_summary');
        }
        container.find('.insight').corner();
        container.find('.insight_footer table').corner('bottom');
        container.jScrollPane( { topCapHeight:40, bottomCapHeight:40 } );
        var target_insight = getURLParameter('insight');
        if (target_insight != 'null')
            $('#timeline')[0].scrollTo('#' + target_insight);
    };
    
    var methods =
    {
        init:function()
        {
            var insights_timeline = this;
            var username = $('#page').data('username');
            $.get('/community/insights/load/' + username, function(data) { render_insight_timeline(data, insights_timeline); }, 'JSON');
        }
    };

    $.fn.profile_page_insights_timeline = function(method)
    {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.profile_page_insights_timeline' );
    };
})(jQuery);