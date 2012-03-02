(function($)
{
    var run_helpers = function()
    {
        Tipped.create('.tool_tip');
        $('.corner, .chart_display img, .treding_row1 img, .treding_row2 img, .treding_row3 img, .remixes img, .like_links table, .border').corner('6px');
        $('.button').button();
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
                                '/delv/remixes/' + insight_id + '/5',
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
        var insight_id = link.data('insight_id');
        var like_links = $('#like_links_' + insight_id);
        if (link.is('.open'))
        {
            link.removeClass('open');
            like_links.slideUp();
        }
        else
        {
            link.addClass('open');
            like_links.slideDown();

        }
    };

    var show_templates_click = function(event, link)
    {
        if (link.is('.open'))
        {
            $('.insight_template').slideUp();
            link.removeClass('open');
            link.html('Show Templates');
        }
        else
        {
            $('.insight_template').slideDown();
            link.addClass('open');
            link.html('Hide Templates');
        }
    }

    var init_social_buttons = function()
    {
        /*Facebook*/
        (function(d, s, id) {
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) return;
            js = d.createElement(s); js.id = id;
            js.src = "//connect.facebook.net/en_GB/all.js#xfbml=1&appId=" + FACEBOOK_APP_ID;
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
        //$('.activity').jScrollPane();
        $('.remixes_link').click(function(event){remixes_click(event, $(this));});
        $('.like_link').click(function(event){like_click(event, $(this));});
        $('.show_templates').click(function(event){show_templates_click(event, $(this)); })
    };
})(jQuery);