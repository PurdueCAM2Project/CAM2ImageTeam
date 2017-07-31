/**
 * This jQuery script checks the width of the screen in rems to see 
 * if it's mobile and provides sliding functionality on the menu.
 */
$(document).ready(function()
{
    // Anything less than this width is counted as a "mobile" display
    var WIDTH_MOBILE_IN_REMS = 70; // If you change this, change main.css, too
    
    // Since no one should be messing with the <html> element's font-size, this == 1 rem
    var PX_PER_REM = parseInt($("html").css("font-size"));

    var screenWidthInRems = $(window).width() / PX_PER_REM;

    if (screenWidthInRems <= WIDTH_MOBILE_IN_REMS)
    {
        // This menu is displayed by default because it needs to display if JS is disabled
        $("#nav-content").delay(250).slideUp(500);
        $("#menu-icon-clickme").css({"font-style": "normal"});
    }

    // Nav menu toggle on click event.  The menu icon changes italics, too
    $("#menu-icon-clickme").click(function()
    {
        if ($("#nav-content").is(":visible"))
        {
            $(this).css({"font-style": "normal"});
            $("#nav-content").slideUp(500);
        }
        else
        {
            $(this).css({"font-style": "italic"});
            $("#nav-content").slideDown(500);
        }
    });
});