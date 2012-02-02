(function( $ ){

    var methods =
    {
        init:function(dashboard)
        {
            var insight_container = this;
            insight_container.data('dashboard', dashboard);
            return insight_container;
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
                            return insight_container.insight('_render_short_summary_for_visualization');
            insight_container.insight('_render_short_summary_for_data');
            return insight_container;
        },
        render_thumbnail:function()
        {
            return this.insight('_render', { width:100, height:75, class_name:'thumbnail' });
        },
        render_medium:function()
        {
            return this.insight('_render', { width:300, height:225, class_name:'medium' });
        },
        _render:function(data)
        {
            var insight_container = this;
            var width = data.width;
            var height = data.height;
            var class_name = data.class_name;
            var dashboard = insight_container.data('dashboard');
            var visualization = null;
            for (var x=0; x<dashboard.collections.length; x++)
                if (dashboard.collections[x].visualizations != null && dashboard.collections[x].visualizations.length > 0)
                    for (var y=0; y<dashboard.collections[x].visualizations.length; y++)
                        if (dashboard.collections[x].visualizations[y].configured)
                            visualization = dashboard.collections[x].visualizations[y].snapshot;
            var insight_inner_container = $('<a href="/community/' + dashboard.username + '?insight=' + dashboard.id + '" class="insight_' + class_name + '" title="' + dashboard.username + " - " + dashboard.name + " - last accessed " + dashboard.last_saved_pretty + '"></div>');
            if (visualization != null)
            {
                insight_inner_container.append('<canvas width="'+ width + 'px" height="' + height + 'px"></canvas>');
                insight_container.append(insight_inner_container);
                canvg(insight_container.find('canvas')[0], visualization, { scaleWidth:width, scaleHeight:height, ignoreMouse:true});
                insight_inner_container.corner();
                Tipped.create(insight_inner_container);
            }
            else
            {
                var data_logos = [];
                for (var x=0; x<dashboard.collections.length; x++)
                    for (var y=0; y<dashboard.collections[x].data_points.length; y++)
                        if (data_logos.length < 9)
                            data_logos[data_logos.length] = (width > 150)
                                ? dashboard.collections[x].data_points[y].image_large
                                : dashboard.collections[x].data_points[y].image_medium;
                insight_container.append(insight_inner_container);
                for (var y=0; y<data_logos.length; y++)
                    insight_inner_container.append("<img src='" + data_logos[y] + "' />");
                insight_inner_container.addClass('images_' + data_logos.length);
                insight_inner_container.corner();
                Tipped.create(insight_inner_container);
            }
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
            if (svg != null && svg != '')
            {
                canvg(insight_container.find('canvas')[0], svg, { scaleWidth:486, scaleHeight:220, ignoreMouse:true});
            }
            else
            {
                var parent = insight_container.find('canvas').parent();
                parent.children().remove();
                parent.append('<img class="no_image" src="/static/images/thecommunity/no_profile_image.gif" />');
            }
            return insight_container.insight('_apply_insight_actions');
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
            return insight_container.insight('_apply_insight_actions');
        },
        _apply_insight_actions:function()
        {
            var insight_container = this;
            var dashboard = insight_container.data('dashboard');
            insight_container.find('.delete').click
                (
                    function(event)
                    {
                        event.preventDefault();
                        $.get('/dashboard/delete/' + dashboard.id);
                        $(this).parents('li.dashboard').fadeOut();
                        setTimeout( function() {$('#profile_page').profile_page('render');}, 500);
                    }
                );
            if ($('body').data('username') == dashboard.username)
                insight_container.find('.remix').remove();
            else
                insight_container.find('.edit').remove();
            return insight_container;
        }
    };

    $.fn.insight = function(method)
    {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.profile_page_insights_timeline_insight_container' );
    }
})(jQuery);