(function($)
{
    $.fn.header = function()
    {
        var header = this;
        header.find('#personal_menu_link')
            .mouseover
            (
                function()
                {
                    header.find('#personal_menu').slideDown();
                }
            );
        header.find('#personal_menu')
            .mouseleave
            (
                function()
                {
                    header.find('#personal_menu').slideUp();
                }
            );
    }
})(jQuery);