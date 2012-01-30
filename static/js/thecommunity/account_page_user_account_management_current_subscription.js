/***********************************************************************************************************************
 user_account_management_current_subscription
 ***********************************************************************************************************************/
(function ( $ )
{
    $.fn.user_account_management_current_subscription = function()
    {
        var current_subscription_container = this;
        current_subscription_container.children().remove();
        var handle_get_return_function = function(container, template)
        {
            $(container).html(template);
        };
        $.get('/community/current_subscription', function(data) { handle_get_return_function(current_subscription_container, data); });
    }
})( jQuery );