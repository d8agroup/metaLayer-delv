/***********************************************************************************************************************
SITE WIDE FUNCTIONS
***********************************************************************************************************************/
function guid()
{
    return 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace
    (
        /[xy]/g,
        function(c)
        {
            var r = Math.random()*16|0,v=c=='x'?r:r&0x3|0x8;return v.toString(16);
        }
    );
}

function clone(object)
{
    var newObj = (object instanceof Array) ? [] : {};
    for (i in object)
    {
        if (i == 'clone')
            continue;
        if (object[i] && typeof object[i] == "object")
            newObj[i] = clone(object[i]);
        else
            newObj[i] = object[i];
    }
    return newObj;
};

function display_time(time)
{
    var d = new Date(time * 1000);
    return d.toUTCString();
}

function wait(ms)
{
    ms += new Date().getTime();
    while (new Date() < ms){}
}

function apply_waiting(element, text)
{
    var waiting_template = $.tmpl('waiting_large', {text:text});
    element.append(waiting_template);
    waiting_template.css({ opacity:0.7,top:0, width:element.outerWidth(), height:element.outerHeight() });
    waiting_template.find('p').css({ top:(element.height() / 2) });
}

function remove_waiting(element)
{
    element.find('.waiting').remove();
}

function apply_tipped(elements)
{
    Tipped.create(elements);
}

function apply_helper_class_functions(element)
{
    element.find('.helper_corner').corner();
    Tipped.create(element.find('.tool_tip'));
    element.find('.tool_tip_ajax').each
    (
        function(i, e)
        {
            var tipped_function = function(element)
            {
                Tipped.create
                (
                    element,
                    '/dashboard/ajax_bridge',
                    {
                        ajax:
                        {
                            data:'request_url=' + $(element).attr("title") + '&csrfmiddlewaretoken=' + $('#csrf_form input').val(),
                            type:'POST'
                        }
                    }
                );
            };
            setTimeout(function() { tipped_function(e); }, 500);
        }
    );

    //Tipped.create(element.find('.tool_tip_ajax'), {ajax:true});
}

function clean_user_generated_html(element)
{
    element.find('a').each
    (
        function()
        {
            $(this).attr('target', '_blank');
        }
    )
}

$(document).ready
(
    function()
    {
        /* Waiting Large Area*****************************************************************/
        $.template
        (
            'waiting_large',
            "<div class='waiting waiting_large'>" +
                "<p>{{html text}}<img src='/static/images/site/loading_circle.gif' /></p>" +
            "</div>"
        );

        $.get('/static/html/parts/dashboard_search_widget_search_filters.html', function(t) { $.template('dashboard_search_widget_search_filters', t)});
        $.get('/static/html/parts/user_account_management.html', function(t) { $.template('user_account_management', t)});
        $.get('/static/html/parts/user_dashboard_management.html', function(t) { $.template('user_dashboard_management', t)});
        $.get('/static/html/parts/user_dashboard_management_saved_dashboards.html', function(t) { $.template('user_dashboard_management_saved_dashboards', t)});
        $.get('/static/html/parts/user_dashboard_management_saved_dashboards_not_allowed.html', function(t) { $.template('user_dashboard_management_saved_dashboards_not_allowed', t)});
        $.get('/static/html/parts/user_dashboard_management_dashboard_templates.html', function(t) { $.template('user_dashboard_management_dashboard_templates', t)});

        setTimeout(function(){ $('#page').site(); }, 1000);
        Tipped.setDefaultSkin('light');
    }
);