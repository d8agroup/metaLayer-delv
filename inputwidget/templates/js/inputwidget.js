var URL_SAVE_CONFIG = '/inputs/configure';
var URL_RELOAD_INPUT_WIDGET = '/inputs/render';
var URL_ADD_NEW_INPUT = '/inputs/add';
var URL_CLEAR_CONFIG = '/inputs/clearconfig';
var URL_REMOVE_INPUT = '/inputs/remove';

$(document).ready
(
	function()
	{
		ApplyInputWidgetDroppable();
	}
);

function SaveInputWidgetConfig(collection_id)
{
	config_elements = $('#' + collection_id + ' .input_widget_config input');
	query_string = [];
	for(var x=0; x<config_elements.length; x++)
		query_string.push($(config_elements[x]).attr('name') + "=" + encodeURIComponent($(config_elements[x]).val()) + "");
	query_string = query_string.join('&');
	$.get
	(
		URL_SAVE_CONFIG + "?" + query_string,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	)
}

function ApplyInputWidgetDroppable()
{
	/* APPLY TO THE EMPTY INPUT WIDGET SLOTS */
	$('.input_widget_droppable').droppable
	(
		{
			activeClass:'input_widget_droppable_active',
			hoverClass:'input_widget_droppable_hover',
			drop:function(event, ui)
			{
				var draggable = ui.draggable;
				var droppable = $(this);
				var collection_id = droppable.parents('.collection').attr('id');
				var input_type = draggable.find('.type').html();
				$.get
				(
					URL_ADD_NEW_INPUT + "?collection_id=" + collection_id + "&type=" + input_type,
					function()
					{
						var outer_droppable = $('#' + collection_id + " .input_widget_container");
						outer_droppable.removeClass('input_widget_droppable');
						outer_droppable.droppable('destroy');
						ReloadInputWidget(collection_id);
					}
				)
			}
		}
	);
}

function ReloadInputWidget(collection_id)
{
	$.get
	(
		URL_RELOAD_INPUT_WIDGET + "?collection_id=" + collection_id,
		function(template)
		{
			var input_widget_container = $('#' + collection_id + " .input_widget_container");
			input_widget_container.children().remove();
			input_widget_container.append(template);
			ApplyInputWidgetDroppable();
		}
	)
}

function ReconfigureInput(collection_id, input_id, input_type)
{
	$.get
	(
		URL_CLEAR_CONFIG + "?collection_id=" + collection_id + "&input_id=" + input_id + "&input_type=" + input_type,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	);
}

function RemoveInput(collection_id, input_id)
{
	$.get
	(
		URL_REMOVE_INPUT + "?collection_id=" + collection_id + "&input_id=" + input_id,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	);
}