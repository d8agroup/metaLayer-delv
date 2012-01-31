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
                if (dashboard.collections[x].visualizations != null && dashboard.collections[x].visualizations.length > 0)
                    for (var y=0; y<dashboard.collections[x].visualizations.length; y++)
                        if (dashboard.collections[x].visualizations[y].configured)
                            return insight_container.profile_page_insights_timeline_insight_container('_render_short_summary_for_visualization');
            insight_container.profile_page_insights_timeline_insight_container('_render_short_summary_for_data');
            return insight_container;
        },
        _render_short_summary_for_visualization:function()
        {
            var insight_container = this;
            var dashboard = insight_container.data('dashboard');
            var template_data =
            {
                insight:dashboard
            };
            var svg = '';
            for (var x=0; x<dashboard.collections.length; x++)
                for (var y=0; y<dashboard.collections[x].visualizations.length; y++)
                    svg = dashboard.collections[x].visualizations[y].snapshot;

            var insight_html = $.tmpl('short_summary_for_visualization', template_data);
            insight_container.html(insight_html);
            canvg(insight_container.find('canvas')[0], svg, { scaleWidth:486, scaleHeight:220, ignoreMouse:true});
            return insight_container.profile_page_insights_timeline_insight_container('_apply_insight_actions');
        },
        _render_short_summary_for_data:function()
        {
            var insight_container = this;
            var dashboard = insight_container.data('dashboard');
            var data_logos = [];
            for (var x=0; x<dashboard.collections.length; x++)
                for (var y=0; y<dashboard.collections[x].data_points.length; y++)
                    data_logos[data_logos.length] = dashboard.collections[x].data_points[y].image_large;
            var template_data =
            {
                insight:dashboard,
                insight_images:data_logos
            };
            var insight_html = $.tmpl('short_summary_for_data', template_data);
            insight_container.html(insight_html);
            return insight_container.profile_page_insights_timeline_insight_container('_apply_insight_actions');
        },
        _apply_insight_actions:function()
        {
            var insight_container = this;
            var dashboard = insight_container.data('dashboard');
            insight_container.find('.insight_actions .edit').button();
            return insight_container;
        }
    };

    $.fn.profile_page_insights_timeline_insight_container = function(method)
    {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.profile_page_insights_timeline_insight_container' );
    }
})(jQuery);