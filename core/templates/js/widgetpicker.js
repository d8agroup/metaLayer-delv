$(document).ready
(
	function()
	{
		ApplyDraggable()
	}
)



function ApplyDraggable()
{
	$('.draggable_widget').draggable
	(
		{ 
			revert:true, 
			helper:"clone", 
			zIndex: 350,
            start: function() { $(this).toggle(); },
            stop: function() { $(this).toggle(); }  
		}
	);
}