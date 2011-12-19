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
            function(event)
            {
                event.preventDefault();
                unconfigured_data_point_html.find('.errors').remove();
                for (var x=0; x < data_point.elements.length; x++)
                    data_point.elements[x]['value'] = search_widget_container.find('.data_point_config form .form_row .' + data_point.elements[x].name).val();
                $.post
                (
                    '/dashboard/data_points/validate',
                    { data_point:JSON.stringify(data_point), csrfmiddlewaretoken:$('#csrf_form input').val() },
                    function(data)
                    {
                        var passed = data.passed;
                        if (passed)
                        {
                            data_point['configured'] = true;
                            $.post
                            (
                                '/dashboard/data_points/get_configured_name',
                                { data_point:JSON.stringify(data_point), csrfmiddlewaretoken:$('#csrf_form input').val() },
                                function(data)
                                {
                                    data_point['configured_display_name'] = data.configured_display_name;
                                    $.post('/dashboard/data_points/add_data_point', { data_point:JSON.stringify(data_point), csrfmiddlewaretoken:$('#csrf_form input').val() })
                                    search_widget_container.parents('.collection_container').dashboard_collection('render');
                                }
                            );
                        }
                        else
                        {
                            unconfigured_data_point_html.find('.instructions').before
                            (
                                "<div class='alert errors'>" +
                                    "<p>Sorry, we couldn't save this data point, please review the errors below</p>" +
                                "</div>"
                            );
                            for (var error_group in data.errors)
                            {
                                var error_html = $("<div class='errors alert'></div>");
                                for (var x=0; x<data.errors[error_group].length; x++)
                                    error_html.append("<p>" + data.errors[error_group][x] + "</p>");
                                unconfigured_data_point_html.find('.form_row .' + error_group).parents('.form_row').prepend(error_html);
                            }
                        }
                    },
                    'JSON'
                );
                return search_widget_container;
            }
        );

        search_widget_container.html(unconfigured_data_point_html);
    }
})( jQuery );
