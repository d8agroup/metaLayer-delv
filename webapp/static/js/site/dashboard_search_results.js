/***********************************************************************************************************************
 DASHBOARD - dashboard_search_results
 ***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var search_results = data.search_results;
            var search_filters = data.search_filters;
            if ($.isEmptyObject(search_results))
                return this.dashboard_search_results('render_waiting');
            this.data('search_results', search_results);
            this.data('search_filters', search_filters);
            return this.dashboard_search_results('render');
        },
        render_waiting:function()
        {
            var search_results_container = this;
            search_results_container.children().remove();
            $.tmpl('waiting_large').appendTo(this);
            return this;
        },
        render:function()
        {
            var search_results_container = this;
            var search_results = search_results_container.data('search_results');
            var search_filters = search_results_container.data('search_filters');

            search_results_container.children().remove();

            var search_results_header_html = $('<div class="search_results_header"></div>');
            search_results_container.append(search_results_header_html.dashboard_search_results_header({search_results:search_results, search_filters:search_filters}));

            var search_results_content_items_html = $('<ul class="content_items"></ul>');
            search_results_container.append(search_results_content_items_html.dashboard_search_results_content_items(search_results));

            return search_results_container;
        },
        search_results_updated:function()
        {
            return this;
        }
    }

    $.fn.dashboard_search_results = function( method ){
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );}
})( jQuery );