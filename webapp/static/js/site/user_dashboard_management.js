/***********************************************************************************************************************
 user_dashboard_management
***********************************************************************************************************************/
(function ( $ )
{
    $.fn.user_dashboard_management = function()
    {
        /*** START Embedded functions ***/
        var render_user_dashboard_management = function(container, data)
        {
            var maximum_number_of_saved_dashboards = data.maximum_number_of_saved_dashboards;
            if (maximum_number_of_saved_dashboards == 0)
            {
                container.find('#saved_dashboards_container').user_dashboard_management_saved_dashboards_not_allowed();
                container.find('#dashboard_templates_container').user_dashboard_management_clickable_dashboard_templates();
            }
            else
            {
                container.find('#saved_dashboards_container').user_dashboard_management_saved_dashboards(data);
                container.find('#dashboard_templates_container').user_dashboard_management_draggable_dashboard_templates();
            }
        };
        /*** END Embedded functions ***/

        var user_dashboard_management_container = this;
        user_dashboard_management_container.html($.tmpl('user_dashboard_management'));
        $.get
            (
                '/user/dashboard_management/saved_dashboards',
                function(data) { render_user_dashboard_management(user_dashboard_management_container, data)}
            );
    }
})( jQuery );