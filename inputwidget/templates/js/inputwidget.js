var URL_SAVE_CONFIG = '/inputs/configure';
var URL_RELOAD_INPUT_WIDGET = '/inputs/render';
var URL_ADD_NEW_INPUT = '/inputs/add';
var URL_CLEAR_CONFIG = '/inputs/clearconfig';
var URL_REMOVE_INPUT = '/inputs/remove';
var URL_ADD_NEW_ACTION = '/actions/add';
var URL_MOVE_INPUT_WIDGET = '/inputs/move';
var URL_COLLAPSE = '/inputs/collapse';
var URL_EXPAND = '/inputs/expand';

$(document).ready
(
	function()
	{
		ApplyInputWidgetDroppable();
		ApplyInputWidgetDraggable();
		setTimeout
		(
			function()
			{
				var collections = $('.collection');
				for(var x=0; x<collections.length; x++)
				{
					var collection_id = $(collections[x]).attr('id');
					RefreshAll(collection_id);
				}
			},
			60000
		);
	}
);

function RemoveInputWidget(collection_id)
{
	var collection = $('#' + collection_id);
	collection.children().remove()
	collection.append(HTML_ADD_INPUT_WIDGET)
	ApplyInputWidgetDroppable()
	$.get(URL_REMOVE_INPUT + "?collection_id=" + collection_id)
}

function ToggleInputWidget(collection_id)
{
	var collection = $('#' + collection_id);
	var button = collection.find('.toggle_button img');
	var content = collection.find('.content');
	
	if (content.is(':visible'))
	{
		content.slideUp();
		button.attr('src', '/media/images/icon-max.png');
		button.attr('alt', 'Maximise');
		$.get(URL_COLLAPSE + "?collection_id=" + collection_id);
	}
	else
	{
		content.slideDown();
		button.attr('src', '/media/images/icon-min.png');
		button.attr('alt', 'Minimise');
		$.get(URL_EXPAND + "?collection_id=" + collection_id);
	}
}

function RefreshAll(collection_id)
{
	if ($('#' + collection_id + ' .input_widget').length > 0 && $('#' + collection_id + ' .reloading').length == 0)
	{
		$('#' + collection_id).draggable('destroy');
		$('#' + collection_id).droppable('destroy');
		ShowReloadingForInputWidget(collection_id)
		var reload_func = function() { ReloadInputWidget(collection_id, true); }
		setTimeout(reload_func, 5000);
	}
	var func = function() { RefreshAll(collection_id); }
	setTimeout(func, 60000);
}

function SaveInputWidgetConfig(collection_id)
{
	config_elements = $('#' + collection_id + ' .input_widget_config input');
	query_string = [];
	for(var x=0; x<config_elements.length; x++)
		query_string.push($(config_elements[x]).attr('name') + "=" + encodeURIComponent($(config_elements[x]).val()) + "");
	query_string = query_string.join('&');
	
	ShowLoadingForInputWidget(collection_id);
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
	var input_widget_containers = $('.input_widget_container');
	for (var x=0; x<input_widget_containers.length; x++)
	{
		var container = $(input_widget_containers[x]);
		if (container.find('.drop_prompt').lenght == 0)
			container.removeClass('input_widget_droppable').addClass('input_or_action_widget_droppable');
	}
	
	
	/* APPLY TO THE EMPTY INPUT WIDGET SLOTS */
	$('.input_widget_droppable').droppable
	(
		{
			activeClass:'input_widget_droppable_active',
			hoverClass:'input_widget_droppable_hover',
			accept:'.input_draggable, .input_widget',
			drop:function(event, ui)
			{
				var draggable = ui.draggable;
				var droppable = $(this);
				var collection_id = droppable.parents('.collection').attr('id');
				ShowLoadingForInputWidget(collection_id);
				if(draggable.is('.input_widget'))
				{
					var new_collection_id = collection_id;
					var old_collection_id = draggable.parents('.collection').attr('id');
					$.get
					(
						URL_MOVE_INPUT_WIDGET + '?new_collection_id=' + new_collection_id + "&old_collection_id=" + old_collection_id,
						function()
						{
							ReloadInputWidget(new_collection_id);
							draggable.remove();
							var old_collection = $('#' + old_collection_id); 
							old_collection.children().remove()
							old_collection.append(HTML_ADD_INPUT_WIDGET)
							var new_collection = $('#' + new_collection_id);
							new_collection.find('.input_widget_container').removeClass('input_widget_droppable').addClass('input_or_action_widget_droppable');
							ApplyInputWidgetDroppable()						
						}
					)
				}
				else
				{
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
		}
	);

	$('.input_or_action_widget_droppable').droppable
	(
		{
			activeClass:'input_widget_droppable_active',
			hoverClass:'input_widget_droppable_hover',
			accept:'.input_draggable, .action_draggable, .input_widget',
			drop:function(event, ui)
			{
				var draggable = ui.draggable;
				var droppable = $(this);
				var collection_id = droppable.parents('.collection').attr('id');
				var input_type = draggable.find('.type').html();
				ShowLoadingForInputWidget(collection_id);
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
				else if(draggable.is('.input_widget'))
				{
					var new_collection_id = collection_id;
					var old_collection_id = draggable.parents('.collection').attr('id');
					$.get
					(
						URL_MOVE_INPUT_WIDGET + '?new_collection_id=' + new_collection_id + "&old_collection_id=" + old_collection_id,
						function()
						{
							ReloadInputWidget(new_collection_id);
							draggable.remove();
							var collection = $('#' + old_collection_id); 
							collection.children().remove()
							collection.append(HTML_ADD_INPUT_WIDGET)
							ApplyInputWidgetDroppable()						
						}
					)
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
	
	$('.visual_droppable').droppable
	(
		{
			activeClass:'visual_widget_droppable_active',
			hoverClass:'visual_widget_droppable_hover',
			accept:'.visual_draggable',
			drop:function(event, ui)
			{
				var draggable = ui.draggable;
				
				if(draggable.is('.map_widget'))
				{
					alert('Sorry, this type of visual widget is not avaliable in this release');
					return;
				}
				
				var droppable = $(this);
				var collection_id = droppable.parents('.collection').attr('id');
				var visual_type = draggable.find('.type').html();
				var url = '/widget/visualwidgets/' + visual_type + '/add_new?collection_id=' + collection_id;
				var loading_html = $("<div class='loading' style='margin:10px 0;'><img src='/media/images/loading_bar.gif' style='margin:20px 0'/></div>");
				droppable.after(loading_html);
				droppable.remove();
				$.get
				(
					url,
					function()
					{
						ReloadInputWidget(collection_id);
					}
				);
			}
		}
	);
	
	$('.output_droppable').droppable
	(
		{
			activeClass:'output_widget_droppable_active',
			hoverClass:'output_widget_droppable_hover',
			accept:'.output_draggable',
			drop:function(event, ui)
			{
				var draggable = ui.draggable;
				
				if(draggable.is('.sendemail_widget'))
				{
					alert('Sorry, this type of output widget is not avaliable in this release');
					return;
				}
				
				var droppable = $(this);
				var collection_id = droppable.parents('.collection').attr('id');
				var type = draggable.find('.type').html();
				var url = '/widget/outputwidgets/' + type + '/add_new?collection_id=' + collection_id;
				var loading_html = $("<div class='loading' style='margin:10px 0;'><img src='/media/images/loading_bar.gif' style='margin:20px 0'/></div>");
				droppable.after(loading_html);
				droppable.remove();
				$.get
				(
					url,
					function()
					{
						ReloadInputWidget(collection_id);
					}
				);
			}
		}
	);
}

function ApplyInputWidgetDraggable()
{
	$('.input_widget').draggable
	(
		{
			revert:true,
			handle:'.inputs',
			stack:'.input_widget',
			start:function()
			{
				$(this).parents('.input_widget_container').droppable('destroy');
			},
			stop:function()
			{
				ApplyInputWidgetDroppable();
				ApplyInputWidgetDraggable();
				ApplyDraggable(); //this calls the elements in the widgetpicker to ensure z axis
			}
		}
	);
}

function ReloadInputWidget(collection_id, polling)
{
	/*
	if (polling != true)
		ShowLoadingForInputWidget(collection_id);
	*/
	$.get
	(
		URL_RELOAD_INPUT_WIDGET + "?collection_id=" + collection_id,
		function(template)
		{
			if (!$(template).is('.input_widget_config') && !$(template).is('.action_widget_config'))
			{	
				if($(template).find('.inputs ul.full li').length == 0)
				{
					var collection = $('#' + collection_id); 
					collection.children().remove();
					collection.append(HTML_ADD_INPUT_WIDGET);
					ApplyInputWidgetDroppable();
					return;
				}
			}
			
			var input_widget_container = $('#' + collection_id + " .input_widget_container");
			input_widget_container.children().remove();
			input_widget_container.append(template);
			ApplyInputWidgetDroppable();
			ApplyInputWidgetDraggable();
			ApplyDraggable(); //this calls the elements in the widgetpicker to ensure z axis
			ApplyUIElements();
			RunVisualJS(collection_id);
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
	var loading_html = $("<div class='loading'><img src='/media/images/loading_bar.gif' style='margin:125px 0;'/></div>");
	input_widget_container.children().remove();
	input_widget_container.append(loading_html);
}

function ShowReloadingForInputWidget(collection_id)
{
	var input_widget_container = $('#' + collection_id + " .input_widget_container");
	input_widget_container.prepend("<div class='reloading'><span>reloading</span><img src='/media/images/loading_bar.gif' /></div>")
}

function ReconfigureInput(collection_id, input_id, input_type)
{
	ShowLoadingForInputWidget(collection_id);
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
	ShowLoadingForInputWidget(collection_id);
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
	ShowLoadingForInputWidget(collection_id);
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
	ShowLoadingForInputWidget(collection_id);
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
	var form = $('#' + collection_id + ' .action_widget_config form');
	var type = form.find('input.type').val();
	var query_string = form.serialize();
	
	ShowLoadingForInputWidget(collection_id);
	
	$.get
	(
		'/widget/actionwidgets/' + type + "/save_config?" + query_string,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	)
}

function RunVisualJS(collection_id)
{
	$('#' + collection_id + ' .refresh_link').each
	(
		function()
		{
			var link_url = $(this).html();
			link_url = link_url.replace(/\&amp;/g, "&");
			$.getScript(link_url);
		}	
	);
}

function RemoveVisualWidget(collection_id, visual_id, visual_type)
{
	url = '/widget/visualwidgets/' + visual_type + '/remove?collection_id=' + collection_id + '&visual_id=' + visual_id;
	$.get
	(
		url,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	);
}

function ReconfigureVisualWidget(collection_id, visual_id, visual_type)
{
	url = '/widget/visualwidgets/' + visual_type + '/clear_config?collection_id=' + collection_id + '&visual_id=' + visual_id;
	$.get
	(
		url,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	);
}

function SaveVisualConfig(collection_id, visual_type, visual_id, config_type)
{
	url = '/widget/visualwidgets/' + visual_type + '/configure?collection_id=' + collection_id + '&visual_id=' + visual_id + '&type=' + config_type;
	$.get
	(
		url,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	);
}

function RemoveOutputWidget(collection_id, output_id, output_type)
{
	$('.' + output_id).remove();
	url = '/widget/outputwidgets/' + output_type + '/remove?collection_id=' + collection_id + '&output_id=' + output_id;
	$.get
	(
		url,
		function()
		{
			ReloadInputWidget(collection_id);
		}
	);
}
