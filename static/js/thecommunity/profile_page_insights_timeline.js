(function( $ ){

    var start_new_insight_clicked = function(event, container)
    {
        $.get
            (
                '/user/dashboard_management/new_dashboard_from_template/1',
                function(data)
                {
                    $.get
                        (
                            '/dashboard/load/' + data.dashboard_id,
                            function(data)
                            {
                                var li = $('<li class="dashboard"></li>');
                                li.append('<div class="widgets"></div>');
                                li.append('<div class="collections"></div>');
                                container.find('ul#timeline').prepend(li);
                                li.dashboard({'dashboard':data.dashboard});
                            },
                            'JSON'
                        );
                }
            )

    };

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
            insights_timeline.find('#start_new_insight').click ( function(event) { start_new_insight_clicked(event, insights_timeline); } );
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