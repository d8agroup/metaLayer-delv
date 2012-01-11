/***********************************************************************************************************************
 DASHBOARD - dashboard_search_widget_control_panel
***********************************************************************************************************************/
(function( $ )
{
    $.fn.dashboard_search_widget_options_panel = function(options)
    {
        this.append
        (
            '<a class="close_collection tipped" title="remove this collection from your dashboard">' +
                '<img src="/static/images/site/icon_cross.png" />' +
            '</a>' +
            '<img src="/static/images/site/icon_drag.png" title="click and drag this search box" class="drag_handle tipped" />'
        );
        this.find('a.close_collection').click
        (
            function()
            {
                $(this).parents('.collection_container').dashboard_collection('remove');
            }
        );
        Tipped.create(this.find('.tipped'));
        return this;
    };
})( jQuery );

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

            var options = configuration.options;
            var options_container_html = $("<div class='options_container'></div>");
            this.append(options_container_html.dashboard_search_widget_options_panel(options));

            var data_points = configuration.data_points;
            var data_points_container_html = $("<div class='data_points_container'></div>");
            this.append(data_points_container_html.dashboard_search_widget_data_points(data_points));

            this.dashboard_search_widget('search_results_updated');

            return this;
        },
        search_results_updated:function()
        {
            var configuration = this.data('configuration');
            this.find('.search_results_container').remove();
            var search_results = configuration.search_results;
            var search_filters = configuration.search_filters;
            var search_results_html = $("<div class='search_results_container'></div>");
            this.append(search_results_html.dashboard_search_results({search_results:search_results, search_filters:search_filters}));

            return this;
        }
    }

    $.fn.dashboard_search_widget = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );