(function( $ ){
    $.fn.account_page = function()
    {
        var account_page = this;
        account_page.find('#account_management_container').user_account_management();
    };
})( jQuery );

var account = {
   
   facebook: {
      
      init: function() {
         FB.Event.subscribe('auth.authResponseChange', function(response) {

           if (response.authResponse && response.status == "connected") {

               // user has chosen to link their Facebook profile to this account

               $.ajax({
                  type: "POST",
                  url: "/community/save_facebook_profile",
                  data: "facebook_id=" + response.authResponse.userID + "&access_token=" + response.authResponse.accessToken,
                  dataType: "json",
                  success: function(response) {
                     $("#associate_facebook_profile").text("Linked to Facebook");

                     $(".profile_pic").css("background-image", "url('" + window.location.protocol + "//" + response.profile_picture + "')");
                  },
                  error: function(response) {
                     alert('An error occurred when linking Facebook profile.');
                  }
               });
            }

         });
         
      },
      
      sign_in: function(requested_permissions) {
         FB.login(function(response) {}, { scope: requested_permissions });
      }
   },
   
   twitter: {
      sign_in: function() {
         twttr.anywhere(function (T) { 
            T.signIn();
            
            T.bind("authComplete", function(e, user){ 
               // triggered when auth completed successfully
               alert(user.screenName);
               
               // user has chosen to link their Twitter profile to this account
               
               $.ajax({
                  type: "POST",
                  url: "/community/save_twitter_profile",
                  data: "screen_name=" + user.screenName,
                  dataType: "json",
                  success: function(response) {
                     $("#associate_twitter_profile").text("Linked to Twitter");

                     $(".profile_pic").css("background-image", "url('" + window.location.protocol + "//" + response.profile_picture + "')");
                  },
                  error: function(response) {
                     alert('An error occurred when linking Twitter profile.');
                  }
               });
               
            }); 
         });
      }
   }
   
}
