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
            /*
            if (CONTENT_ITEM_TEMPLATES[content_item_template_key] != null)
            {
                rendered_content_items[x] = $.tmpl(CONTENT_ITEM_TEMPLATES[content_item_template_key], content_items[x]);
            }
            else
            {
                ready_to_render = false;
                $.get
                (
                    '/dashboard/data_points/get_content_item_template/' + content_items[x]['channel_type'] + '/' + content_items[x]['channel_sub_type'],
                    function(data)
                    {
                        var template = data.template;
                        var template_name = 'dashboard_search_results_content_items_' + content_item_template_key;
                        $.template(template_name, template);
                        CONTENT_ITEM_TEMPLATES[content_item_template_key] = template_name;
                        rendered_content_items[x] = $.tmpl(template_name, content_items[x]);
                        ready_to_render = true;
                    }
                )
            }
            */
        }
        /*
        while(!ready_to_render) {}
        debugger;
        for (var x=0; x<rendered_content_items.length; x++)
            this.append(rendered_content_items[x]);
        */
        return this;
    }
})( jQuery );