(function($)
{
    var run_helpers = function()
    {
        Tipped.create('.tool_tip');
        $('.corner, .chart_display img, .treding_row1 img, .treding_row2 img, .treding_row3 img, .remixes img').corner('6px');
    };

    var remixes_click = function(event, link)
    {
        var insight_id = link.data('insight_id');
        var remixes = $('#remixes_' + insight_id);
        if (link.is('.open'))
        {
            link.removeClass('open');
            remixes.slideUp();
        }
        else
        {
            link.addClass('open');
            remixes.slideDown
                (
                    function()
                    {
                        remixes.load
                            (
                                '/community/remixes/' + insight_id + '/5',
                                function()
                                {
                                    run_helpers();
                                }
                            );
                    }
                );

        }
    };

    var like_click = function(event, link)
    {
        link.parents('.insight').find('.like_modal').dialog
            (
                {
                    modal:true,
                    height:400,
                    width:600
                }
            );

    };

    var init_social_buttons = function()
    {
        /*Facebook*/
        (function(d, s, id) {
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) return;
            js = d.createElement(s); js.id = id;
            js.src = "//connect.facebook.net/en_GB/all.js#xfbml=1&appId=140737952711154";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
        /*twitter*/
        !function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");
        /*google+*/
        (function() {
            var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
            po.src = 'https://apis.google.com/js/plusone.js';
            var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
        })();
    }

    $.fn.profile_page = function(data)
    {
        run_helpers();
        init_social_buttons();
        $('.remixes_link').click(function(event){remixes_click(event, $(this));});
        $('.like_link').click(function(event){like_click(event, $(this));});
    };
})(jQuery);