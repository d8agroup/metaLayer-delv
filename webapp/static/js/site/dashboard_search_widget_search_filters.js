/***********************************************************************************************************************
 DASHBOARD - dashboard_search_widget_search_filters
 ***********************************************************************************************************************/
(function( $ )
{
    $.fn.dashboard_search_widget_search_filters = function(data)
    {
        var search_results = data.search_results;
        var search_filters = data.search_filters;

        var search_filters_container = this;

        search_filters_container.children().remove();

        search_filters_container.data('search_results', search_results);
        search_filters_container.data('search_filters', search_filters);

        var keywords_mask = 'filter by keywords';

        var template_data = {
            keywords:(search_results.keywords == '') ? keywords_mask : search_results.keywords,
            pagination:search_results.pagination,
            items_shown:(search_results.pagination.total > search_results.pagination.pagesize) ? search_results.pagination.pagesize : search_results.pagination.total
        }

        $.tmpl('dashboard_search_widget_search_filters', template_data).appendTo(search_filters_container);

        search_filters_container.find('.keywords_container').corner();
        search_filters_container.find('.keywords_container input')
            .focus
            (
                function()
                {
                    var input = $(this);
                    if (input.val() == keywords_mask)
                        input.val('')
                }
            )
            .blur
            (
                function()
                {
                    var input = $(this);
                    if (input.val() == '')
                        input.val(keywords_mask)
                }
            )
            .keypress
            (
                function(e)
                {
                    if (e.which == 13)
                    {
                        e.preventDefault();
                        var input = $(this);
                        if (input.val() == '')
                            input.parents('.keywords_container').find('.remove_keyword_filter').click();
                        else
                            input.parents('.keywords_container').find('.apply_keyword_filter').click();
                    }
                }
            )
            .blur();

        search_filters_container.find('.apply_keyword_filter').click
            (
                function()
                {
                    var keywords = $(this).parents('.keywords_container').find('input').val();
                    if (keywords == keywords_mask)
                        return;
                    search_filters_container.data('search_filters')['keywords'] = keywords;
                    $(this).parents('.collection_container').dashboard_collection('render');
                }
            );

        search_filters_container.find('.remove_keyword_filter').click
            (
                function()
                {
                    search_filters_container.data('search_filters')['keywords'] = '';
                    $(this).parents('.collection_container').dashboard_collection('render');
                }
            );
        return this
    }
})( jQuery );
