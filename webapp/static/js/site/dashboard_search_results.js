/***********************************************************************************************************************
TEMPLATES
***********************************************************************************************************************/
$(document).ready
(
    function()
    {
        /* dashboard_search_results_header *****************************************************************/
        $.template
        (
            'dashboard_search_results_header',
            "<div class='pagination'>" +
                "<a class='filters_link'>filters&darr;</a>" +
                "<p class='total'>${pagination.total} items found</p>" +
            "</div>" +
            "<div class='filters hidden'>" +
                "<p>Use these filters to dive into your data</p>" +
                "<div class='filter_row keywords'>" +
                    "<p class='filter_name'>Keywords</p>" +
                    "<input type='text' value='${keywords}' />" +
                "</div>" +
                "<div class='filter_actions'>" +
                    "<input type='button' class='reset' value='reset'/>" +
                    "<input type='button' class='update' value='update'/>" +
                "</div>" +
            "</div>"
        );
        /* dashboard_search_results_content_item *****************************************************************/
        $.template
        (
            'dashboard_search_results_content_item',
            "<li class='content_item'>" +
                "<p class='date'>${date}</p>" +
                "<p class='title'>${title}</p>" +
                "<div class='text_container'>" +
                    "{{each text}}<div class='text_item'>{{html $value}}</div>{{/each}}" +
                "</div>" +
            "</li> "
        );
    }
);

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

/***********************************************************************************************************************
 DASHBOARD - dashboard_search_results_content_items
***********************************************************************************************************************/
(function( $ )
{
    $.fn.dashboard_search_results_content_items = function(data)
    {
        var content_items = data.content_items;
        $.tmpl('dashboard_search_results_content_item', content_items).appendTo(this);
        return this;
    }
})( jQuery );

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