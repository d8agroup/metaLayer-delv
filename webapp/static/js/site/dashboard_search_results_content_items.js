/***********************************************************************************************************************
 DASHBOARD - dashboard_search_results_content_items
 ***********************************************************************************************************************/

var CONTENT_ITEM_TEMPLATES = {};

(function( $ )
{
    $.fn.dashboard_search_results_content_items = function(data)
    {
        var ready_to_render = true;
        var content_items = data.content_items;
        var rendered_content_items = [];
        for (var x=0; x<content_items.length; x++)
        {
            var template_name = 'dashboard_search_results_content_items_' + content_items[x]['channel_type'] + "_" + content_items[x]['channel_sub_type'];
            $.tmpl(template_name, content_items[x]).appendTo(this);
        }
        clean_user_generated_html(this);
        apply_helper_class_functions(this);
        return this;
    }
})( jQuery );