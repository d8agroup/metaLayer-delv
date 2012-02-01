(function( $ )
    {
        var methods =
        {
            init:function(data)
            {
                var header = this;
                var dashboard = data.dashboard;
                header.data('dashboard', dashboard);
                header.find('#logo_container').append("<input type='text' id='dashboard_name'/>")
                this.find('#dashboard_name').header_dashboard_name(dashboard);

                this.find('a').click
                (
                    function(e)
                    {
                        $('.visualizations_container').dashboard_visualizations('capture_snapshots');
                        $('.dashboard').dashboard('save');
                        return true;
                    }
                );
            },
            dashboard_saved:function()
            {
                var header = this;
                if (header.find('.saving').length > 0)
                    return;
                var saving_html = $("<span class='saving'>Saving ...</span>");
                header.find('#logo_container').append(saving_html);
                saving_html.fadeIn();
                setTimeout
                    (
                        function()
                        {
                            saving_html.fadeOut
                                (
                                    function()
                                    {
                                        saving_html.remove();
                                    }
                                );
                        },
                        2000
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