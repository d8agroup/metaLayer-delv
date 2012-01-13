/***********************************************************************************************************************
 DASHBOARD - dashboard_search_widget_control_panel
 ***********************************************************************************************************************/
(function( $ )
{
    $.fn.dashboard_search_widget_options_panel = function(options)
    {
        this.append
            (
                '<a class="refresh_data tipped" title="toggle automatic refreshing of data">' +
                    '<img src="/static/images/site/icon_clock.png" />' +
                '</a> ' +
                '<a class="explore_data tipped" title="explore this data - click to show/hide filters">' +
                    '<img src="/static/images/site/icon_search.png" />' +
                '</a> ' +
                '<a class="close_collection tipped" title="remove this collection from your dashboard">' +
                    '<img src="/static/images/site/icon_cross.png" />' +
                '</a>'
            );
        this.find('a.refresh_data').click
            (
                function()
                {
                    alert('TODO: This is not yet active');
                }
            );
        this.find('a.explore_data').click
            (
                function()
                {
                    var search_filters = $(this).parents('.search_widget').find('.search_filters');
                    if (search_filters.is(':visible'))
                        search_filters.slideUp();
                    else
                        search_filters.slideDown();
                }
            );
        this.find('a.close_collection').click
            (
                function()
                {
                    $(this).parents('.collection_container').dashboard_collection('remove');
                }
            );
        var tipped_elements = this.find('.tipped');
        setTimeout( function() {apply_tipped(tipped_elements); tipped_elements=null}, 500);
        return this;
    };
})( jQuery );
