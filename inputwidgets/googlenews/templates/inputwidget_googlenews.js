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

function InputwidgetGooglenewsSaveConfig(collection_id)
{
	var value = encodeURIComponent($('#'+ collection_id).find('.search').val())
	var url = '/widget/inputwidgets/googlenews' 
	var widget = $('#'+ collection_id).find('.input_widget_googlenews')
	$.get
	(
		url + '/save_config?search=' + value + "&collection=" + collection_id,
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

function ReconfigureGooglenewsWidget(collection_id)
{
	var url = '/widget/inputwidgets/googlenews' 
	var widget = $('#'+ collection_id).find('.input_widget_googlenews')
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
