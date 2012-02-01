(function( $ ){
    $.fn.account_page = function()
    {
        var account_page = this;
        account_page.find('#account_management_container').user_account_management();
    };
})( jQuery );