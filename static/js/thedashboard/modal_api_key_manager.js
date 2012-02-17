(function($)
{
    var render_api_keys = function(data)
    {
        var api_keys = data.api_keys;
        $('#api_key_manager .waiting').hide();
        $('#api_key_manager .api_key_line_container').append($.tmpl('api_key_line', api_keys))
    };

    $.fn.modal_api_key_manager = function()
    {
        var modal = this;
        modal.find('.waiting').show();
        modal.find('.api_key_line_container').children().remove();
        modal.dialog
            (
                {
                    modal:true,
                    minHeight:300,
                    width:600,
                    buttons:
                    {
                        'Save and Exit':function()
                        {
                            var inputs = $('#api_key_manager .api_key_line input');
                            var return_data = [];
                            for (var x=0; x<inputs.length; x++)
                                if ($(inputs[x]).val() > '')
                                    return_data.push($(inputs[x]).attr('name') + "=" + $(inputs[x]).val())
                            $.get('/dashboard/api_keys/save?' + return_data.join('&'));
                            $(this).dialog('close');
                            $('.dashboard_collection').dashboard_collection('render');
                        }
                    }
                }
            );

        $.get('/dashboard/api_keys/load', function(data) { render_api_keys(data); });
    }
})(jQuery);