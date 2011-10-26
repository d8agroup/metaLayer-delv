var HTML_EMPTY_COLLECTION = "<div class='collection'></div>"
var HTML_ADD_INPUT_WIDGET = "<div class='input_widget_droppable input_widget_container'><p class='drop_prompt'>Drag an input widget here to start a new collection</p></div>"
//var HTML_INPUT_WIDGET_CONTAINER = "<div class='input_widget_container'></div>"

$(document).ready
(
	function ()
	{
		LoadWidgetPicker();
		LoadCollections();
		ClearCollectionConfig();
		ApplyUIElements();
	}
)

function LoadWidgetPicker()
{
	var widget_picker = $('#widget_picker')
	var widget_picker_render_url = '/core/widgetpicker/render'
	var widget_picker_script_url = '/core/widgetpicker/script'
	$.get
	(
		widget_picker_render_url,
		function(return_data)
		{
			widget_picker.children().remove()
			widget_picker.append(return_data.template)
			$.getScript(widget_picker_script_url)
			widget_picker.slideDown()
			ApplyUIElements();
		}
	)
}

function LoadCollections()
{
	var content = $('#content')

	for (var x=1; x<5; x++)
	{
		var empty_collection = $(HTML_EMPTY_COLLECTION)
		var empty_input_widget = $(HTML_ADD_INPUT_WIDGET)
		content.append(empty_collection.attr('id', 'collection' + x).append(empty_input_widget))
	}
}

function ClearCollectionConfig()
{
	$.get('/config/clear');
}

function ApplyUIElements()
{
	$('.button').button();
	$('.tabs').tabs();
	$('.accordion').accordion();
}