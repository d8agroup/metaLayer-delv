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

$(document).ready
(
    function()
    {
        $('#page').site();
    }
)
/***********************************************************************************************************************
SITE WIDE TEMPLATES
***********************************************************************************************************************/
$(document).ready
(
    function()
    {
        /* Waiting Large Area*****************************************************************/
        $.template
        (
            'waiting_large',
            "<div class='waiting waiting_large'>" +
                "<p>WAITING ...</p>" +
            "</div>"
        );

        $.get('/static/html/parts/dashboard_search_results_header.html', function(t) { $.template('dashboard_search_results_header', t)});
    }
);