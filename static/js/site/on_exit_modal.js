(function($)
{
    var methods =
    {
        init:function()
        {
            var on_exit_modal = this;
            on_exit_modal.jqm({modal:true, overlay:80});
            on_exit_modal.find('.back, .save').button();
            on_exit_modal.find('.radio').buttonset();
            on_exit_modal.find('.save').click
                (
                    function()
                    {
                        var dashboard = $('.dashboard').data('dashboard');
                        dashboard.name = on_exit_modal.find('.name input').val();
                        if (dashboard.config == null)
                            dashboard.config = {};
                        dashboard.config.live = ($('.live input[type=radio]:checked').attr('id') == 'keep_running_yes');
                        dashboard.config.description = on_exit_modal.find('.description textarea').val();
                        if (dashboard.config.categories == null)
                            dashboard.config.categories = []
                        on_exit_modal.find('.categories input:checked').each
                            (
                                function()
                                {
                                    dashboard.config.categories[dashboard.config.categories.length] = $(this).parent('li').find('label').html()
                                }
                            );


                        for (var x=0; x<dashboard.collections.length; x++)
                            dashboard.collections[x].search_results = [];
                        var post_data = { dashboard:JSON.stringify(dashboard), csrfmiddlewaretoken:$('#csrf_form input').val() };
                        $('#waiting_modal').jqm({modal:true, overlay:80});
                        $('#waiting_modal').jqmShow();
                        $.ajax
                            (
                                {
                                    async:false,
                                    url:'/dashboard/save',
                                    type:'POST',
                                    data:post_data
                                }
                            );
                        return true;
                    }
                );
            on_exit_modal.find('.back').click
                (
                    function()
                    {
                        on_exit_modal.jqmHide();
                    }
                )
        },
        open:function(data)
        {
            var dashboard = data.dashboard;
            var on_exit_modal = this;
            if (dashboard.config == null)
                dashboard.config = {};

            on_exit_modal.find('.name input').val(dashboard.name);
            if (dashboard.config.description != null)
                on_exit_modal.find('.description textarea').val(dashboard.config.description);
            if (dashboard.config.live != null && dashboard.config.live)
            {
                on_exit_modal.find('#keep_running_yes').attr('checked', true);
                on_exit_modal.find('#keep_running_no').attr('checked', false);
            }
            if (dashboard.config.categories != null)
            {
                for (var x=0; x<dashboard.config.categories.length; x++)
                {
                    var category_name = dashboard.config.categories[x];
                    on_exit_modal.find('.categories label').each
                        (
                            function()
                            {
                                if ($(this).html() == category_name)
                                    $(this).parent('li').find('input').attr('checked', true);
                            }
                        );
                }
            }
            on_exit_modal.find('.radio').buttonset();
            //on_exit_modal.find('.categories input').button();
            on_exit_modal.jqmShow();
        }
};
    $.fn.on_exit_modal = function( method )
    {
        // Method calling logic
        if ( methods[method] )
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        else if ( typeof method === 'object' || ! method )
            return methods.init.apply( this, arguments );
        else
            $.error( 'Method ' +  method + ' does not exist on jQuery.on_exit_modal' );
    }
})(jQuery);