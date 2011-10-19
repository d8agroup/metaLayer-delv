$(document).ready
(
	function()
	{
		LoadConfigTabs()
		ApplyButtonEffects()
	}
)

function LoadConfigTabs()
{
	if ($('.inputwidget_config').length == 0)
		return
		
	$('.inputwidget_config .tabs').tabs()
}

function ApplyButtonEffects()
{
	$('.button').button()
}

function InputwidgetTwitterSaveConfig(collection_id, type)
{
	var value = encodeURIComponent($('#'+ collection_id).find('.' + type).val())
	var url = '/widget/inputwidgets/twitter' 
	var widget = $('#'+ collection_id).find('.input_widget_twitter')
	$.get
	(
		url + '/save_config?' + type + '=' + value + "&collection=" + collection_id,
		function(return_data)
		{
			if (return_data['status'] == 'error')
			{
				alert('error')
			}
			else
			{
				$.get
				(
					url + '/render?collection=' + collection_id,
					function(return_data)
					{
						widget.slideUp()
						widget.after(return_data)
						widget.remove()
						$.getScript(url + '/render_js?collection=' + collection_id)
					}
				)
			}
		},
		'JSON'
	)
}

function ReconfigureTwitterWidget(collection_id)
{
	var url = '/widget/inputwidgets/twitter' 
	var widget = $('#'+ collection_id).find('.input_widget_twitter')
	$.get
	(
		url + '/reconfigure?collection=' + collection_id,
		function()
		{
			$.get
			(
				url + '/render?collection=' + collection_id,
				function(return_data)
				{
					widget.slideUp()
					widget.after(return_data)
					widget.remove()
					$.getScript(url + '/render_js?collection=' + collection_id)
				}
			)
		}
	)
}
