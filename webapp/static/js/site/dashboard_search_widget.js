/***********************************************************************************************************************
 DASHBOARD - dashboard_search_widget
***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(configuration)
        {
            this.data('configuration', configuration);
            this.dashboard_search_widget('render');
            return this;
        },
        render:function()
        {
            var configuration = this.data('configuration');

            this.children().remove();

            for (var x=0; x<configuration.data_points.length; x++)
                if (!configuration.data_points[x].configured)
                {
                    var unconfigured_data_point_html = $("<div class='data_point_config_container'></div>");
                    this.html(unconfigured_data_point_html);
                    unconfigured_data_point_html.dashboard_unconfigured_data_point(configuration.data_points[x]);
                    return this;
                }

            var options = configuration.options;
            var options_container_html = $("<div class='options_container'></div>");
            this.append(options_container_html.dashboard_search_widget_options_panel(options));

            var data_points = configuration.data_points;
            var data_points_container_html = $("<div class='data_points_container'></div>");
            this.append(data_points_container_html.dashboard_search_widget_data_points(data_points));

            var search_filters_html = $('<div class="search_filters"></div>');
            this.append(search_filters_html);

            var search_results_html = $("<div class='search_results_container'></div>");
            this.append(search_results_html);

            this.dashboard_search_widget('run_search', { first_run:true });

            return this;
        },
        run_search:function(data)
        {
            var search_widget = this;
            var search_results_html = this.find('.search_results_container');

            if (data.first_run)
            {
                var search_results_loading_html = $
                    (
                        "<div class='waiting waiting_large'>" +
                            "<p>Reloading Results<img src='/static/images/site/loading_circle.gif' /></p>" +
                        "</div>"
                    );
                search_results_html.append(search_results_loading_html);
                search_results_loading_html.fadeIn();
            }
            else
            {
                search_widget.find('.options_container .refresh_data img').attr
                    (
                        'src',
                        '/static/images/site/icon_clock_loading.gif'
                    )
                    .addClass('loading');
            }

            var really_run_search_function = function(search_widget)
            {
                var configuration = search_widget.data('configuration');
                if (configuration != null)
                    $.post
                    (
                        '/dashboard/run_search',
                        {
                            data_points:JSON.stringify(configuration.data_points),
                            search_filters:JSON.stringify(configuration.search_filters),
                            csrfmiddlewaretoken:$('#csrf_form input').val()
                        },
                        function(data)
                        {
                            var search_results = data.search_results;
                            configuration.search_results = search_results;
                            var search_filters = configuration.search_filters;
                            search_widget.find('.search_results_container').dashboard_search_results({search_results:search_results, search_filters:search_filters});
                            search_widget.find('.search_filters').dashboard_search_widget_search_filters({search_results:search_results, search_filters:search_filters});
                            search_widget.find('.search_results_container').jScrollPane
                                (
                                    {
                                        topCapHeight:40,
                                        bottomCapHeight:40
                                    }
                                );
                            search_widget.find('.options_container .refresh_data img').attr
                                (
                                    'src',
                                    '/static/images/site/icon_clock.png'
                                )
                                .removeClass('loading');
                            var run_search_at_interval_function = function(search_widget)
                            {
                                search_widget.dashboard_search_widget('run_search', { first_run:false });
                            };

                            setTimeout(function() { run_search_at_interval_function(search_widget) }, 20000);
                        }
                    );
            };

            setTimeout(function() { really_run_search_function(search_widget); }, 2000);
            return this;
        },
        remove_data_point:function(data_point_id)
        {
            var configuration = this.data('configuration');
            var new_data_points = [];
            for (var x=0; x<configuration.data_points.length; x++)
                if (configuration.data_points[x].id != data_point_id)
                    new_data_points[new_data_points.length] = configuration.data_points[x];
            this.data('configuration').data_points = new_data_points;
            this.parents('.collection_container').dashboard_collection('render');
            return this;
        }
    }

    $.fn.dashboard_search_widget = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );