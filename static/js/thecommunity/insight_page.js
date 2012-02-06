(function($)
{
    var render_search_results_function = function(data, configuration)
    {
        var search_results_container = $('#' + configuration.id + ' .search_results_container');
        search_results_container.children().remove();
        var search_results_list = $("<ul class='search_results'></ul>");
        search_results_container.append(search_results_list);
        var content_items = data.search_results.content_items;
        for (var x=0; x<content_items.length; x++)
        {
            var template_name = 'dashboard_search_results_content_items_' + content_items[x]['channel_type'] + "_" + content_items[x]['channel_sub_type'];
            $.tmpl(template_name, content_items[x]).appendTo(search_results_list);
        }
        search_results_list.jScrollPane( { topCapHeight:40, bottomCapHeight:40 } );
        clean_user_generated_html(search_results_list);
        apply_helper_class_functions(search_results_list);
    };

    var run_search = function(configuration)
    {
        $.post
            (
                '/dashboard/run_search',
                {
                    data_points:JSON.stringify(configuration.data_points),
                    search_filters:JSON.stringify(configuration.search_filters),
                    csrfmiddlewaretoken:$('#csrf_form input').val()
                },
                function(data) { render_search_results_function(data, configuration); }
            );
    };

    var load_data_point_content_template = function(data)
    {
        var template = data.template;
        var template_name = 'dashboard_search_results_content_items_' + data.type + '_' + data.sub_type;
        $.template(template_name, template);
    };

    $.fn.insight_page = function(insight)
    {
        var insight_page = this;
        insight_page.find('#trending_insights').insights_trending_insights(9);
        var collections_container = insight_page.find('#collections_container');
        for (var c=0; c<insight.collections.length; c++)
        {
            var collection = insight.collections[c];
            if (collection.data_points == null || collection.data_points.length == 0)
                continue;
            var collection_html = $("<div class='collection' id='" + collection.id + "'></div>");
            collections_container.append(collection_html);
            
            for (var v=0; v<collection.visualizations.length; v++)
            {
                var visualization = collection.visualizations[v];
                var visualization_container = $("<div class='visualization' id='" + visualization.id + "'></div>");
                collection_html.append(visualization_container);
                var timestamp = new Date;
                timestamp = timestamp.getTime();
                $.ajax
                    (
                        {
                            async:true,
                            type:'POST',
                            url:'/dashboard/visualizations/run_visualization/' + timestamp,
                            data:
                            {
                                visualization:JSON.stringify(visualization),
                                data_points:JSON.stringify(collection.data_points),
                                search_filters:JSON.stringify(collection.search_filters),
                                csrfmiddlewaretoken:$('#csrf_form input').val()
                            },
                            dataType:'script'
                        }
                    );
            }
            
            
            var search_widget_header_html = $("<div class='search_widget_header'></div>");
            collection_html.append(search_widget_header_html);
            for (var dp=0; dp<collection.data_points.length; dp++)
            {
                var data_point = collection.data_points[dp];
                var load_template_url = '/dashboard/data_points/get_content_item_template/' + data_point.type + '/' + data_point.sub_type;
                $.get ( load_template_url, function(data) { load_data_point_content_template(data); } );
                search_widget_header_html.append
                    (
                        "<img src='"+ data_point.image_small +"' title='" + data_point.configured_display_name + "'/>"
                    );
            }
            var search_results_html = $("<div class='search_results_container'></div>");
            search_results_html.append("<div class='waiting'>Loading <img src='/static/images/thecommunity/loading_circle.gif'></div>")
            collection_html.append(search_results_html);

            var run_search_function = function(collection)
            {
                return function() { run_search(collection); }
            };
            setTimeout(run_search_function(collection), 2000);
        }
        insight_page.find('.collection').addClass('collection_' + $('.collection').length);
    };
})(jQuery);