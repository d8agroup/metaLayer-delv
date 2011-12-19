/** DASHBOARD - unconfigured data point *******************************************************************************/
(function( $ )
{
    $.fn.dashboard_unconfigured_data_point = function(data_point)
    {
        var search_widget_container = this;
        var unconfigured_data_point_html = $("<div class='data_point_config'>" +
                                                "<div class='image_and_title'>" +
                                                    "<img src='" + data_point.image_large + "' />" +
                                                    "<h3>" + data_point.full_display_name + "</h3>" +
                                                "</div>" +
                                                "<p class='instructions'>" + data_point.instructions + "</p>" +
                                                "<form>" +
                                                    '<div class="form_actions">'+
                                                        '<input type="submit" name="cancel" class="cancel" value="remove"/>' +
                                                        '<input type="submit" name="save"  class="save" value="save"/>' +
                                                    '</div>' +
                                                "</form>" +
                                            "</div>");

        for (var x=0; x<data_point.elements.length; x++)
        {
            var element = data_point.elements[x];
            unconfigured_data_point_html.find('form').prepend
            (
                "<div class='form_row'>" +
                    "<label>" + element.display_name + "</label>" +
                    '<input type="' + element.type + '" name="' + element.name + '" class="' + element.name + '" value="' + element.value + '"/>' +
                    '<p class="help">' + element.help + '</p>' +
                '</div>'
            );
        }

        unconfigured_data_point_html.find('.cancel').click
        (
            function()
            {
                search_widget_container.parents('.collection_container').dashboard_collection('remove_data_point', data_point.id);
                search_widget_container.parents('.collection_container').dashboard_collection('render');
                return search_widget_container;
            }
        );
        unconfigured_data_point_html.find('.save').click
        (
            function()
            {
                data_point['configured'] = true;
                for (var x=0; x < data_point.elements.length; x++)
                    data_point.elements[x]['value'] = search_widget_container.find('.data_point_config form .form_row .' + data_point.elements[x].name).val();
                search_widget_container.parents('.collection_container').dashboard_collection('render');
                return search_widget_container;
            }
        );

        search_widget_container.html(unconfigured_data_point_html);
    }
})( jQuery );
