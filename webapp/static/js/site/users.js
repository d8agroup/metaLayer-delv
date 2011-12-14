/***********************************************************************************************************************
Dashboard Templates
***********************************************************************************************************************/
(function( $ )
{
    $.fn.dashboard_template = function()
    {
        var id = this.attr('id');
        this.find('a.load_template').click
        (
            function()
            {
                $('#page').site('show_dashboard');
                setTimeout
                (
                    function()
                    {
                        $.get
                        (
                            '/user/new_dashboard_from_template/' + id,
                            function(data)
                            {
                                $('#page').site('load_dashboard', { dashboard_id:data.dashboard_id })
                            },
                            'JSON'
                        );
                    },
                    500
                );
            }
        )
    }
})( jQuery );

(function( $ )
{
    $.fn.dashboard_template_list = function()
    {
        var container = this;
        container.html('loading ...');
        $.get
        (
            '/user/dashboard_templates',
            function(template)
            {
                container.html(template);
                container.find('.dashboard_template').dashboard_template();
            }
        );
    }
})( jQuery );

/***********************************************************************************************************************
 saved_dashboard
***********************************************************************************************************************/
(function( $ )
{
    $.fn.saved_dashboard = function()
    {
        var id = this.attr('id');
        this.find('a.load_dashboard').click
        (
            function()
            {
                $('#page').site('show_dashboard');
                setTimeout
                (
                    function()
                    {
                        $('#page').site('load_dashboard', { dashboard_id:id})
                    },
                    500
                );
            }
        )
    }
})( jQuery );

(function( $ )
{
    $.fn.saved_dashbaord_list = function()
    {
        var container = this;
        container.html('loading ...');
        $.get
        (
            '/user/saved_dashbaords',
            function(template)
            {
                container.html(template);
                container.find('.dashboard_summary').saved_dashboard();
            }
        );
    }
})( jQuery );

/***********************************************************************************************************************
user_home
***********************************************************************************************************************/
(function ( $ )
{
    var methods =
    {
        init:function()
        {
            this.user_home('refresh');
        },
        refresh:function()
        {
            this.find('#saved_dashboards .list-container').saved_dashbaord_list();
            this.find('#dashboard_templates .list-container').dashboard_template_list();
        }
    }

    $.fn.user_home = function( method )
    {
        // Method calling logic
        if ( methods[method] )
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method )
            return methods.init.apply( this, arguments );
        else
            $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );
    }
})( jQuery );