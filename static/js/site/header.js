(function( $ )
    {
        var methods =
        {
            init:function()
            {
                this.find('a').click
                (
                    function(e)
                    {
                        $('.visualizations_container').dashboard_visualizations('capture_snapshots');
                        $('.dashboard').dashboard('save');
                        return true;
                    }
                );
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