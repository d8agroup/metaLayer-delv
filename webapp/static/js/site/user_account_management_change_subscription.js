/***********************************************************************************************************************
 user_account_management_change_subscription
 ***********************************************************************************************************************/
(function ( $ )
{
    var methods =
    {
        init:function()
        {
            var change_subscription_container = this;
            change_subscription_container.children().remove();
            apply_waiting(change_subscription_container, 'Reloading Prices');
            var render_service_return_function = function(container, template) { container.html(template); }
            $.get
            (
                '/user/change_subscription',
                function(template)
                {
                    render_service_return_function(change_subscription_container, template);
                    change_subscription_container = null;
                }
            );
        }
    }

    $.fn.user_account_management_change_subscription = function( method )
    {
        // Method calling logic
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );
    }
})( jQuery );