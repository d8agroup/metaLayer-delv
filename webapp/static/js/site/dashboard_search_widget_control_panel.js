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
                    '<img src="/static/images/site/icon_drag.png" title="click and drag this search box" />'
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
