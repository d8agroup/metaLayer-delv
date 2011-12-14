(function( $ )
    {
        var methods =
        {
            init:function()
            {
                this.find('#link_help').click
                (
                    function()
                    {
                        alert('TODO: this needs to open a help modal');
                    }
                );
                this.find('#user_home_link').click
                (
                    function()
                    {
                        $('#page').site('show_user_home');
                    }
                );
            },
            show_user_home_link:function()
            {
                this.find('#user_home_link').show();
            },
            hide_user_home_link:function()
            {
                this.find('#user_home_link').hide();
            }
        }

        $.fn.header = function( method )
        {
            // Method calling logic
            if ( methods[method] )
                return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
            else if ( typeof method === 'object' || ! method )
                return methods.init.apply( this, arguments );
            else
                $.error( 'Method ' +  method + ' does not exist on jQuery.tooltip' );
        }
    }
)( jQuery );