/***********************************************************************************************************************
 DASHBOARD - dashboard_search_results_header
 ***********************************************************************************************************************/
(function( $ )
{
    $.fn.dashboard_search_results_header = function(data)
    {
        var search_results = data.search_results;
        var search_filters = data.search_filters;

        var search_results_header = this;

        search_results_header.data('search_results', search_results);
        search_results_header.data('search_filters', search_filters);

        $.tmpl('dashboard_search_results_header', search_results).appendTo(search_results_header);
        search_results_header.find('a.filters_link').click
            (
                function()
                {
                    var filters = search_results_header.find('.filters');
                    if (filters.is(':visible'))
                    {
                        filters.slideUp();
                        $(this).html("filters&darr;");
                    }
                    else
                    {
                        filters.slideDown();
                        $(this).html("filters&uarr;");
                    }
                }
            );
        search_results_header.find('input.update').click
            (
                function()
                {
                    var keywords = search_results_header.find('.keywords input').val();
                    search_results_header.data('search_filters')['keywords'] = keywords;
                    $(this).parents('.collection_container').dashboard_collection('render');
                }
            );
        search_results_header.find('input.reset').click
            (
                function()
                {
                    var search_filters = search_results_header.data('search_filters');
                    for(var key in search_filters)
                        search_filters[key] = null;
                    $(this).parents('.collection_container').dashboard_collection('render');
                }
            );
        return this;
    }
})( jQuery );
