$(document).ready
(
	function()
	{
		ApplyDraggable()
	}
)



function ApplyDraggable()
{
	$('.draggable_widget').draggable({ revert:true, helper:"clone" })
}