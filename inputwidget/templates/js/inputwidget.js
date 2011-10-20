var URL_SAVE_CONFIG = '/inputs/configure';
var URL_RELOAD_INPUT_WIDGET = '/inputs/render';
var URL_ADD_NEW_INPUT = '/inputs/add';
var URL_CLEAR_CONFIG = '/inputs/clearconfig';
var URL_REMOVE_INPUT = '/inputs/remove';
var URL_ADD_NEW_ACTION = '/actions/add';

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

function CancelInputWidgetConfig(collection_id, input_id)
{
	RemoveInput(collection_id, input_id);
}

function ApplyInputWidgetDroppable()
{
	/* APPLY TO THE EMPTY INPUT WIDGET SLOTS */
	$('.input_widget_droppable').droppable
	(
		{
			activeClass:'input_widget_droppable_active',
			hoverClass:'input_widget_droppable_hover',
			accept:'.input_draggable',
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
						outer_droppable.addClass('input_or_action_widget_droppable')
						ReloadInputWidget(collection_id);
					}
				)
			}
		}
	);

	$('.input_or_action_widget_droppable').droppable
	(
		{
			activeClass:'input_widget_droppable_active',
			hoverClass:'input_widget_droppable_hover',
			drop:function(event, ui)
			{
				var draggable = ui.draggable;
				
				if(!draggable.is('.input_draggable') && !draggable.is('.action_draggable'))
					return;
				
				var droppable = $(this);
				var collection_id = droppable.parents('.collection').attr('id');
				var input_type = draggable.find('.type').html();
				if ( draggable.is('.input_draggable') )
				{
					$.get
					(
						URL_ADD_NEW_INPUT + "?collection_id=" + collection_id + "&type=" + input_type,
						function()
						{
							ReloadInputWidget(collection_id);
						}
					);
				}
				else
				{
					$.get
					(
						'/widget/actionwidgets/' + draggable.find('.type').html() + '/add_new?collection_id=' + collection_id,
						function()
						{
							ReloadInputWidget(collection_id);
						}
					);
				}
			}
		}
	);
}

function ReloadInputWidget(collection_id)
{
	ShowLoadingForInputWidget(collection_id);

	$.get
	(
		URL_RELOAD_INPUT_WIDGET + "?collection_id=" + collection_id,
		function(template)
		{
			var input_widget_container = $('#' + collection_id + " .input_widget_container");
			input_widget_container.children().remove();
			input_widget_container.append(template);
			ApplyInputWidgetDroppable();
			ApplyUIElements();
			input_widget_container.find('.summary').click
			(
				function()
				{
					input_widget_container.find('.summary').slideUp();
					input_widget_container.find('.full').slideDown();
					setTimeout
					(
						function()
						{
							input_widget_container.find('.full').slideUp();
							input_widget_container.find('.summary').slideDown();
						},
						5000
					);
				}
			);
		}
	)
}

function ShowLoadingForInputWidget(collection_id)
{
	var input_widget_container = $('#' + collection_id + " .input_widget_container");
	var height = input_widget_container.height();
	var loading_html = $("<div class='loading' style='height:" + height + "px'><img src='/media/images/loading_bar.gif' style='margin-top:" + parseInt(height/2) + "px'/></div>");
	input_widget_container.children().remove();
	input_widget_container.append(loading_html);
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
		function(return_data)
		{
			if(return_data.was_last_input)
			{
				var collection = $('#' + collection_id); 
				collection.children().remove()
				collection.append(HTML_ADD_INPUT_WIDGET)
				ApplyInputWidgetDroppable()
			}
			else
			{
				ReloadInputWidget(collection_id);
			}
		}
	);
}

function ReconfigureAction(collection_id, action_id, action_type)
{
	$.get
	(
		'/widget/actionwidgets/' + action_type + "/clear_config?collection_id=" + collection_id + "&action_id=" + action_id,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	);
}

function RemoveAction(collection_id, action_id, action_type)
{
	$.get
	(
		'/widget/actionwidgets/' + action_type + "/remove?collection_id=" + collection_id + "&action_id=" + action_id,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	);
}

function CancelActionWidgetConfig(collection_id, action_id, action_type)
{
	RemoveAction(collection_id, action_id, action_type);
}

function SaveActionWidgetConfig(collection_id)
{
	form = $('#' + collection_id + ' .action_widget_config form');
	
	query_string = form.serialize();
	
	$.get
	(
		'/widget/actionwidgets/' + form.find('input.type').val() + "/save_config?" + query_string,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	)
}