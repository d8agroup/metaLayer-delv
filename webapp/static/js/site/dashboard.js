/***********************************************************************************************************************
DASHBOARD - CHECKED 18/01/2010
***********************************************************************************************************************/
(function( $ )
{
    var methods =
    {
        init:function(data)
        {
            var dashboard_container = this;
            var dashboard = data.dashboard;
            dashboard_container.data('dashboard', dashboard);
            dashboard_container.find('#widgets').dashboard_widget_panel({widgets:dashboard.widgets});
            dashboard_container.find('#collections').dashboard_collections_panel({'collections':dashboard.collections});
            return dashboard_container;
        },
        save:function()
        {
            var dashboard = this.data('dashboard');
            var post_data = { dashboard:JSON.stringify(dashboard), csrfmiddlewaretoken:$('#csrf_form input').val() };
            $.post ( '/dashboard/save', post_data );
        }
    };

    $.fn.dashboard = function( method )
    {
        if ( methods[method] ) return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method ) return methods.init.apply( this, arguments );
        else $.error( 'Method ' +  method + ' does not exist on jQuery.dashboard' );
    }
})( jQuery );