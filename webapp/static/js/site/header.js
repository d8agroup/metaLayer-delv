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
                )
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